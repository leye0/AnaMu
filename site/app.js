/* AnaMu Pages — course catalogue, piano roll, and browser MIDI transport. */
"use strict";

const $ = (id) => document.getElementById(id);
const SCHOOLS = {udem:"Université de Montréal",mcgill:"McGill",berklee:"Berklee","berklee-online":"Berklee Online",mit:"MIT OpenCourseWare"};
const SHORT = {udem:"UdeM",mcgill:"McGill",berklee:"Berklee","berklee-online":"Berklee Online",mit:"MIT"};
const STATES = {
  online_demo:["Exemple hors registre","midi"],
  first_learning_analyzed_with_midi:["Écouter un MIDI","midi"],
  first_scope_assessed_without_midi:["Évalué · sans MIDI","assessed"],
  not_yet_assessed:["À analyser","pending"],
  course_choice_placeholder:["Famille d'options","pending"]
};
const COLORS = ["#85e6c9","#aaa1ff","#ffc88c","#80b7ff","#f4a4c9","#eacb7e","#85dbef","#d8b3ff"];
let catalog = [];
let filtered = [];
let current = null;
let docSequence = 0;
const detailCache = new Map();
const midiCache = new Map();
let currentMidi = null;
const playback = {
  context: null, master: null, engine: null, enginePromise: null,
  playing: false, loading: false, request: 0, raf: null,
  position: 0, needsSeek: true
};

function normalize(text) {
  return String(text || "").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
}
function courseFromLink(id) {
  if (!id) return null;
  const exact = catalog.find((entry) => entry.id === id);
  if (exact) return exact;
  // Shared links may use a hyphen where the catalogue uses a space in the code.
  const colon = id.indexOf(":");
  if (colon < 1) return null;
  const institution = id.slice(0,colon).trim().toLowerCase();
  const linkCode = (code) => code.trim().toLowerCase().replace(/[\s-]+/g,"-");
  const code = linkCode(id.slice(colon+1));
  const matches = catalog.filter((entry) => entry.institution === institution && linkCode(entry.code) === code);
  return matches.length === 1 ? matches[0] : null;
}
function formatTime(seconds) {
  const value = Math.max(0, Math.floor(Number(seconds) || 0));
  return Math.floor(value/60) + ":" + String(value%60).padStart(2,"0");
}
function statusLabel(entry) { return (STATES[entry.review_state] || ["À préciser","pending"])[0]; }
function notice(message) { $("message").textContent = message; $("message").hidden = !message; }

function setTag(text, kind) {
  const el = document.createElement("span");
  el.className = "tag" + (kind ? " " + kind : "");
  el.textContent = text;
  $("courseTags").appendChild(el);
}
function drawCourses() {
  const q = normalize($("search").value.trim());
  const school = $("school").value, status = $("status").value;
  filtered = catalog.filter((r) => {
    if (school !== "all" && r.institution !== school) return false;
    if (status === "midi" && !r.midi) return false;
    if (status === "reviewed" && r.review_state !== "first_scope_assessed_without_midi") return false;
    if (status === "pending" && r.review_state !== "not_yet_assessed") return false;
    if (status === "families" && r.review_state !== "course_choice_placeholder") return false;
    if (q && !normalize(r.code + " " + r.title + " " + r.excerpt + " " + SCHOOLS[r.institution]).includes(q)) return false;
    return true;
  });
  $("resultCount").textContent = filtered.length + " entrée" + (filtered.length !== 1 ? "s" : "");
  const list = $("courseList");
  const fragment = document.createDocumentFragment();
  for (const r of filtered) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "course-item" + (current && r.id === current.id ? " selected" : "");
    button.setAttribute("aria-label", r.code + ", " + r.title + ", " + statusLabel(r));
    if (current && r.id === current.id) button.setAttribute("aria-current","true");
    const top = document.createElement("div"); top.className="item-top";
    const code = document.createElement("span"); code.className="item-code"; code.textContent=r.code;
    const inst = document.createElement("span"); inst.className="item-inst"; inst.textContent=SHORT[r.institution] || r.institution;
    top.append(code, inst);
    const title = document.createElement("span"); title.className="item-title";
    const name = r.title.startsWith(r.code + " — ") ? r.title.slice(r.code.length + 3) : r.title;
    title.textContent = name || r.title;
    const meta = document.createElement("div"); meta.className="item-meta";
    const dot = document.createElement("span"); dot.className="item-dot " + (STATES[r.review_state] || STATES.not_yet_assessed)[1];
    const label = document.createElement("span"); label.textContent = statusLabel(r);
    meta.append(dot,label); button.append(top,title,meta);
    button.addEventListener("click", () => showCourse(r.id, true));
    fragment.appendChild(button);
  }
  list.replaceChildren(fragment);
  $("emptyState").hidden = filtered.length !== 0;
  if (!filtered.length) {
    $("detail").hidden = true;
    stopPlayback();
  } else if ($("detail").hidden || !current || !filtered.some((r) => r.id === current.id)) {
    showCourse(filtered[0].id, false);
  }
}

async function getDetail(entry) {
  if (detailCache.has(entry.id)) return detailCache.get(entry.id);
  const response = await fetch("./" + entry.detail, {cache:"no-cache"});
  if (!response.ok) throw Error("Fiche introuvable (" + response.status + ")");
  const data = await response.json();
  detailCache.set(entry.id,data);
  return data;
}
function switchTab(tab) {
  const application = tab === "application";
  $("tabApplication").classList.toggle("active",application);
  $("tabDescription").classList.toggle("active",!application);
  $("tabApplication").setAttribute("aria-selected",String(application));
  $("tabDescription").setAttribute("aria-selected",String(!application));
  $("applicationContent").hidden = !application;
  $("descriptionContent").hidden = application;
}
const comparisonSeekTokens = new WeakMap();
function comparisonPlayAt(audio, seconds) {
  const token = (comparisonSeekTokens.get(audio) || 0) + 1;
  comparisonSeekTokens.set(audio, token);
  const seek = () => {
    if (comparisonSeekTokens.get(audio) === token) audio.currentTime = seconds;
  };
  if (audio.readyState >= 1) seek();
  else audio.addEventListener("loadedmetadata", seek, {once: true});
  return audio.play();
}
function comparisonButton(label, action) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  button.addEventListener("click", action);
  return button;
}
function courseListeningTrial(list, trial) {
  const wrap = document.createElement("details");
  wrap.className = "blind-listening";
  const heading = document.createElement("summary");
  heading.textContent = "Comparer sans les noms · " + trial.title;
  const prompt = document.createElement("p");
  prompt.textContent = trial.question + " L’ordre A/B est tiré au hasard. Ta réponse reste dans cette page.";
  const controls = document.createElement("div");
  controls.className = "audio-cues";
  const votes = document.createElement("div");
  votes.className = "audio-cues";
  const status = document.createElement("p");
  status.setAttribute("role", "status");
  status.textContent = "Lance les deux extraits avant de répondre. Tu peux les réécouter.";
  const audio = document.createElement("audio");
  audio.controls = true;
  audio.preload = "none";
  audio.hidden = true;
  const clips = Math.random() < 0.5 ? [...trial.clips] : [...trial.clips].reverse();
  const heard = [false, false];
  const choices = [];
  let arm = -1;
  let revealed = false;
  audio.addEventListener("play", () => {
    stopPlayback();
    for (const other of list.querySelectorAll("audio")) if (other !== audio) other.pause();
  });
  audio.addEventListener("timeupdate", () => {
    if (arm < 0 || audio.seeking || audio.paused) return;
    const clip = clips[arm];
    if (audio.currentTime >= clip.start + 1 && audio.currentTime <= clip.end + 0.5) {
      heard[arm] = true;
      if (heard.every(Boolean) && !revealed) {
        for (const choice of choices) choice.disabled = false;
        status.textContent = "Choisis une réponse pour révéler les variantes. Il n’y a pas de score.";
      }
    }
    if (audio.currentTime >= clip.end) audio.pause();
  });
  audio.addEventListener("error", () => {
    status.textContent = "L’extrait n’a pas pu être chargé. Réessayer avec A ou B.";
  });
  for (const [i, name] of ["A", "B"].entries()) {
    controls.append(comparisonButton("▶ Extrait " + name, () => {
      audio.pause();
      arm = i;
      const clip = clips[i];
      const source = new URL("./" + clip.url, document.baseURI).href;
      if (audio.src !== source) audio.src = source;
      audio.hidden = false;
      audio.setAttribute("aria-label", "Extrait " + name + " — " + trial.title);
      comparisonPlayAt(audio, clip.start).catch(error => {
        if (error.name !== "AbortError") status.textContent = "Réessaie avec le bouton Lecture du lecteur.";
      });
    }));
  }
  const answers = trial.mode === "difference"
    ? ["J’entends une différence", "Je n’en entends pas", "Incertain"]
    : ["Je préfère A", "Je préfère B", "Pas de préférence / incertain"];
  for (const answer of answers) {
    const button = comparisonButton(answer, () => {
      if (revealed || !heard.every(Boolean)) return;
      revealed = true;
      for (const choice of choices) choice.disabled = true;
      status.textContent = answer + " · A : " + clips[0].label + " · B : " + clips[1].label
        + " · " + trial.explanation;
    });
    button.disabled = true;
    choices.push(button);
    votes.append(button);
  }
  const reset = comparisonButton("Nouvel ordre A/B", () => {
    audio.pause();
    comparisonSeekTokens.set(audio, (comparisonSeekTokens.get(audio) || 0) + 1);
    const replacement = courseListeningTrial(list, trial);
    replacement.open = true;
    wrap.replaceWith(replacement);
    replacement.querySelector("summary").focus();
  });
  const limit = document.createElement("small");
  limit.textContent = "Exercice personnel, sans transmission ni sauvegarde de réponse. Les extraits viennent des rendus continus; le découpage du lecteur n’est pas une isolation acoustique. Les noms restent accessibles dans les fichiers et les autres lecteurs de la fiche.";
  wrap.append(heading, prompt, controls, audio, votes, status, reset, limit);
  wrap.addEventListener("toggle", () => { if (!wrap.open) audio.pause(); });
  return wrap;
}
function showAudioTracks(tracks, trials = [], scores = []) {
  const list = $("audioTracks");
  for (const audio of list.querySelectorAll("audio")) audio.pause();
  list.replaceChildren();
  $("audioSection").hidden = !tracks.length;
  for (const trial of trials) list.append(courseListeningTrial(list, trial));
  for (const score of scores) {
    const box = document.createElement("details");
    box.className = "course-score";
    const heading = document.createElement("summary");
    heading.textContent = "Partition · " + score.title;
    const note = document.createElement("p");
    note.textContent = score.note + " Sur un petit écran, faire défiler la partition horizontalement ou ouvrir la page complète.";
    const links = document.createElement("div");
    links.className = "audio-links";
    const viewer = document.createElement("a");
    viewer.href = "./" + score.viewer;
    viewer.target = "_blank";
    viewer.rel = "noopener";
    viewer.textContent = "Ouvrir la partition et sa légende ↗";
    const xml = document.createElement("a");
    xml.href = "./" + score.musicxml;
    xml.download = "";
    xml.textContent = "MusicXML modifiable ↓";
    links.append(viewer, xml);
    box.append(heading, note, links);
    score.pages.forEach((page, index) => {
      const frame = document.createElement("figure");
      frame.tabIndex = 0;
      frame.setAttribute("aria-label", "Partition, page " + (index + 1) + " — défilement horizontal");
      const image = document.createElement("img");
      image.loading = "lazy";
      image.src = "./" + page;
      image.alt = score.title + " — page " + (index + 1);
      frame.append(image);
      box.append(frame);
    });
    list.append(box);
  }
  for (const track of tracks) {
    const row = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = track.title;
    const audio = document.createElement("audio");
    audio.controls = true;
    audio.preload = "none";
    audio.src = "./" + track.url;
    audio.setAttribute("aria-label",track.title);
    audio.addEventListener("play",() => {
      stopPlayback();
      for (const other of list.querySelectorAll("audio")) {
        if (other !== audio) other.pause();
      }
    });
    const download = document.createElement("a");
    download.className = "download-link";
    download.href = audio.src;
    download.download = "";
    download.textContent = "Télécharger le MP3 ↓";
    download.setAttribute("aria-label","Télécharger le MP3 — " + track.title);
    row.append(title,audio);
    if (track.note) {
      const note = document.createElement("p");
      note.textContent = track.note;
      row.append(note);
    }
    if (track.learning) {
      const question = document.createElement("p");
      question.className = "listening-question";
      question.textContent = track.learning.question;
      row.append(question);
    }
    if (track.cues?.length) {
      row.id = "etude-" + track.id;
      const cues = document.createElement("div");
      cues.className = "audio-cues";
      cues.setAttribute("aria-label", "Comparer les variantes — " + track.title);
      const status = document.createElement("p");
      status.className = "audio-cue-status";
      status.setAttribute("role", "status");
      status.textContent = "Choisir une variante pour écouter ce passage seul.";
      const loopLabel = document.createElement("label");
      loopLabel.className = "audio-loop";
      const loop = document.createElement("input");
      loop.type = "checkbox";
      loopLabel.append(loop, document.createTextNode(" Répéter la variante choisie"));
      const buttons = [];
      let segment = null;
      let pendingSeek = null;
      const clearSegment = () => {
        segment = null;
        for (const b of buttons) b.setAttribute("aria-pressed", "false");
      };
      const seek = (seconds) => {
        if (audio.readyState >= 1) {
          audio.currentTime = seconds;
          pendingSeek = null;
        } else pendingSeek = seconds;
      };
      audio.addEventListener("loadedmetadata", () => {
        if (pendingSeek !== null) seek(pendingSeek);
      });
      const play = () => audio.play().catch(() => {
        pendingSeek = null;
        clearSegment();
        status.textContent = "Lecture impossible. Réessayer avec les commandes audio ou télécharger le MP3.";
      });
      track.cues.forEach((cue, i) => {
        const button = document.createElement("button");
        button.type = "button";
        button.setAttribute("aria-pressed", "false");
        const label = cue.listen_label || cue.label;
        button.textContent = label + " · " + cue.seconds.toLocaleString("fr-CA", {maximumFractionDigits: 3}) + " s";
        button.addEventListener("click", () => {
          clearSegment();
          segment = {start: cue.seconds, end: track.cues[i + 1]?.seconds ?? track.passage_end_seconds ?? track.score_seconds};
          button.setAttribute("aria-pressed", "true");
          status.textContent = label + (loop.checked ? " — en boucle" : " — passage seul");
          seek(segment.start);
          play();
        });
        buttons.push(button);
        cues.append(button);
      });
      audio.addEventListener("timeupdate", () => {
        if (!segment || audio.paused || pendingSeek !== null || audio.currentTime < segment.end) return;
        if (loop.checked) {
          seek(segment.start);
        } else {
          audio.pause();
          clearSegment();
          status.textContent = "Passage terminé. Choisir une autre variante pour comparer.";
        }
      });
      audio.addEventListener("seeking", () => {
        if (segment && (audio.currentTime < segment.start - 0.1 || audio.currentTime > segment.end + 0.1)) {
          clearSegment();
          status.textContent = "Lecture libre depuis la position choisie.";
        }
      });
      audio.addEventListener("error", () => {
        pendingSeek = null;
        clearSegment();
        status.textContent = "Le MP3 n’a pas pu être chargé. Réessayer ou utiliser le lien de téléchargement.";
      });
      const full = document.createElement("button");
      full.type = "button";
      full.textContent = "Écouter l’étude entière";
      full.addEventListener("click", () => {
        clearSegment();
        status.textContent = "Lecture de l’étude entière.";
        seek(0);
        play();
      });
      row.append(cues, loopLabel, full, status);
      const tail = document.createElement("small");
      tail.textContent = "Les passages sont extraits du rendu continu : une résonance du passage précédent peut subsister. La boucle est un repère d’écoute, pas un raccord musical.";
      row.append(tail);
    }
    if (track.learning) {
      const guide = document.createElement("details");
      const summary = document.createElement("summary");
      summary.textContent = "Repères d’analyse et exercice";
      guide.append(summary);
      for (const [label, key] of [["Comparer", "comparison"], ["À essayer", "exercise"], ["Limite", "limit"]]) {
        const p = document.createElement("p");
        const strong = document.createElement("strong");
        strong.textContent = label + " : ";
        p.append(strong, document.createTextNode(track.learning[key]));
        guide.append(p);
      }
      const provenance = document.createElement("small");
      provenance.textContent = "Exercice original AnaMu. Rendu synthétique; aucune validation d’écoute humaine ajoutée.";
      guide.append(provenance);
      row.append(guide);
    }
    const links = document.createElement("div");
    links.className = "audio-links";
    links.append(download);
    if (track.midi_url) {
      const midi = document.createElement("a");
      midi.className = "download-link";
      midi.href = "./" + track.midi_url;
      midi.download = "";
      midi.textContent = "MIDI de cette étude ↓";
      links.append(midi);
      const share = document.createElement("a");
      const url = new URL(window.location.href);
      url.searchParams.set("cours", current.id);
      url.searchParams.set("etude", track.id);
      url.hash = row.id;
      share.href = url.pathname + url.search + url.hash;
      share.textContent = "Lien vers cette étude";
      links.append(share);
    }
    row.append(links);
    list.append(row);
  }
}
async function showCourse(id, historyUpdate) {
  const entry = catalog.find((c) => c.id === id);
  if (!entry) return;
  stopPlayback();
  current = entry;
  const seq = ++docSequence;
  if (historyUpdate) {
    const url = new URL(window.location.href);
    if (url.searchParams.get("cours") !== entry.id) {
      url.searchParams.delete("etude");
      url.hash = "";
    }
    url.searchParams.set("cours",entry.id);
    history.replaceState(null,"",url.pathname+url.search+url.hash);
  }
  $("detail").hidden = false;
  $("emptyState").hidden = true;
  $("courseInstitution").textContent = SCHOOLS[entry.institution] || entry.institution;
  $("courseCode").textContent = entry.code;
  $("courseTitle").textContent = entry.title;
  $("courseExcerpt").textContent = entry.excerpt;
  $("coursePosition").textContent = (catalog.findIndex((r) => r.id === entry.id) + 1) + " / " + catalog.length + " entrées";
  $("courseTags").replaceChildren();
  setTag(statusLabel(entry),entry.midi?"midi":entry.review_state==="first_scope_assessed_without_midi"?"alert":"");
  if (entry.review_state!=="online_demo") {
    setTag(entry.coverage==="usable_first_pass"?"Contenu recensé":entry.coverage==="partial"?"Contenu partiel":"Choix à préciser","violet");
  }
  if (entry.non_algorithmic===true) setTag("Non algorithmique (musique)","alert");
  else if (entry.non_algorithmic===false) setTag("Application algorithmique possible","midi");
  for (const t of entry.algorithmic_tags.slice(0,4)) setTag(t.replace(/_/g," "),"");
  $("descriptionContent").innerHTML = '<p class="missing-description">Chargement de la description…</p>';
  $("applicationContent").innerHTML = '<p class="missing-description">Chargement de l’analyse…</p>';
  showAudioTracks([]);
  $("playerSection").hidden = false;
  $("playerAvailable").hidden = !entry.midi;
  $("playerUnavailable").hidden = !!entry.midi;
  $("playerTag").textContent = entry.midi ? "MIDI original" : "Pas de MIDI";
  $("midiInfo").textContent = "Chargement…";
  $("playBtn").disabled = true;
  $("noMidiReason").textContent = entry.review_state==="not_yet_assessed"
    ? "Cette fiche n'a pas encore été analysée avec le gabarit."
    : entry.review_state==="course_choice_placeholder"
      ? "C'est une famille de choix; il faut identifier le cours exact avant de créer un exemple."
      : "Ce cours est évalué, mais le MIDI ne représenterait pas fidèlement l'apprentissage étudié.";
  switchTab("description");
  currentMidi = null;
  drawRoll();
  drawCoursesActiveOnly();
  notice("");
  try {
    const detail = await getDetail(entry);
    if (seq!==docSequence) return;
    const tracks = detail.audio || [];
    showAudioTracks(tracks, detail.listening_trials || [], detail.scores || []);
    const requestedStudy = new URL(window.location.href).searchParams.get("etude");
    if (requestedStudy && tracks.some(t => t.id === requestedStudy)) {
      document.getElementById("etude-" + requestedStudy)?.scrollIntoView({block: "start"});
    }
    $("playerSection").hidden = !entry.midi && tracks.length > 0;
    $("descriptionContent").innerHTML = detail.overview_html || '<p class="missing-description">Aucune fiche individuelle disponible. Consulter la source officielle et le registre.</p>';
    $("applicationContent").innerHTML = detail.application_html || '<p class="missing-description">L’analyse et la méthode de composition de ce cours restent à documenter. Cette absence ne signifie pas que le cours est dépourvu de contenu musical.</p>';
    $("sourceRepo").hidden = !detail.source_repo; if (detail.source_repo) $("sourceRepo").href=detail.source_repo;
    $("sourceOfficial").hidden = !detail.source_course; if (detail.source_course) $("sourceOfficial").href=detail.source_course;
    if (!entry.midi) {
      $("noMidiReason").textContent = detail.note || $("noMidiReason").textContent;
    } else {
      $("downloadMidi").href="./"+entry.midi;
      $("downloadMidi").download = entry.code.replace(/[^a-z0-9-]/ig,"-")+".mid";
      loadMidi(entry.midi,seq);
    }
    if (detail.application_html) switchTab("application");
  } catch (error) {
    if (seq===docSequence) notice("Impossible de charger la fiche : "+error.message);
  }
}
function drawCoursesActiveOnly() {
  const list=$("courseList");
  for (const button of list.children) {
    // aria-label has code first, but use the button index in the filtered catalog.
    const index=Array.prototype.indexOf.call(list.children,button);
    const selected=filtered[index] && current && filtered[index].id===current.id;
    button.classList.toggle("selected",!!selected);
    if (selected) button.setAttribute("aria-current","true");
    else button.removeAttribute("aria-current");
  }
}

function u32(view,pos) { return view.getUint32(pos,false); }
function textAt(bytes,pos,n) { return String.fromCharCode(...bytes.subarray(pos,pos+n)); }
function varNumber(bytes,p) {
  let value=0,k=0;
  while (p<bytes.length && k++<5) {
    const byte=bytes[p++];
    value=(value<<7)|(byte&127);
    if (!(byte&128)) return [value,p];
  }
  throw Error("Durée variable MIDI invalide");
}
function parseMidi(buffer) {
  const b=new Uint8Array(buffer),view=new DataView(buffer);
  if (b.length<14 || textAt(b,0,4)!=="MThd") throw Error("Le fichier n'est pas un MIDI standard.");
  const headLength=u32(view,4);
  if (headLength<6) throw Error("En-tête MIDI incomplet.");
  const format=view.getUint16(8,false),tracks=view.getUint16(10,false);
  const division=view.getUint16(12,false);
  if (division&0x8000) throw Error("Les timecodes SMPTE MIDI ne sont pas encore pris en charge.");
  const ppq=division,events=[],tempos=[{tick:0,mpq:500000}],markers=[];
  let pos=8+headLength,lastTick=0;
  for (let track=0;track<tracks;track++) {
    if (pos+8>b.length || textAt(b,pos,4)!=="MTrk") throw Error("Piste MIDI invalide.");
    const len=u32(view,pos+4);pos+=8;
    const end=pos+len;if (end>b.length) throw Error("Piste MIDI tronquée.");
    let tick=0,running=0;
    while (pos<end) {
      let delta;[delta,pos]=varNumber(b,pos);tick+=delta;lastTick=Math.max(lastTick,tick);
      if (pos>=end) break;
      let status=b[pos++];
      if (status<128) {
        if (!running) throw Error("Running status MIDI manquant.");
        pos--;status=running;
      } else if(status<0xF0) running=status;
      if (status===0xFF) {
        const type=b[pos++];let size;[size,pos]=varNumber(b,pos);
        if (pos+size>end) throw Error("Métadonnée MIDI tronquée.");
        if (type===0x51 && size===3) {
          const mpq=(b[pos]<<16)|(b[pos+1]<<8)|b[pos+2];
          if (mpq>0) tempos.push({tick,mpq});
        }
        if (type===0x06) markers.push({tick,label:textAt(b,pos,Math.min(size,64))});
        pos+=size;
        if (type===0x2F) {pos=end;break;}
      } else if (status===0xF0 || status===0xF7) {
        let size;[size,pos]=varNumber(b,pos);pos+=size;
      } else if (status>=0xF0) {
        throw Error("Événement système MIDI non géré.");
      } else {
        const kind=status&0xF0,channel=status&0x0F;
        const a=b[pos++],short=kind===0xC0||kind===0xD0,b2=short?0:b[pos++];
        if (kind===0x80 || kind===0x90 || kind===0xC0 || kind===0xB0) {
          events.push({tick,kind,channel,a,b:b2});
        }
      }
    }
    pos=end;
  }
  // Merge tempo changes from every track; all MIDI times are absolute ticks.
  tempos.sort((a,b)=>a.tick-b.tick);
  const clock=(tick)=>{
    let second=0,last=0,mpq=500000;
    for (const item of tempos) {
      if (item.tick>tick) break;
      second+=(item.tick-last)*mpq/(ppq*1000000);
      last=item.tick;mpq=item.mpq;
    }
    return second+(tick-last)*mpq/(ppq*1000000);
  };
  const priority=(e)=>e.kind===0x80||(e.kind===0x90&&e.b===0)?0:e.kind===0xC0?1:2;
  events.sort((a,b)=>a.tick-b.tick||priority(a)-priority(b));
  const programs=new Array(16).fill(0),active=new Map(),notes=[];
  const close=(e)=>{
    const key=e.channel+"-"+e.a,stack=active.get(key);
    if (!stack || !stack.length) return;
    const start=stack.shift();
    if (e.tick>start.tick) {
      notes.push({channel:e.channel,pitch:e.a,velocity:start.velocity,
        program:start.program,startTick:start.tick,endTick:e.tick,
        start:clock(start.tick),end:clock(e.tick)});
    }
  };
  for (const e of events) {
    if (e.kind===0xC0) programs[e.channel]=e.a;
    else if (e.kind===0x90 && e.b>0) {
      const key=e.channel+"-"+e.a;
      if (!active.has(key)) active.set(key,[]);
      active.get(key).push({tick:e.tick,velocity:e.b,program:programs[e.channel]});
    } else if (e.kind===0x80 || e.kind===0x90) close(e);
  }
  // For a poorly terminated note, don't synthesize an endless drone.
  for (const [key,stack] of active) for (const start of stack) {
    const [channel,pitch]=key.split("-").map(Number);
    const endTick=Math.max(start.tick+ppq,lastTick);
    notes.push({channel,pitch,velocity:start.velocity,program:start.program,
      startTick:start.tick,endTick,start:clock(start.tick),end:clock(endTick)});
  }
  notes.sort((a,b)=>a.start-b.start||a.channel-b.channel||a.pitch-b.pitch);
  const duration=Math.max(.5,clock(lastTick),...notes.map(n=>n.end));
  return {format,ppq,tracks,notes,markers:markers.map(m=>({...m,second:clock(m.tick)})),
    duration,channels:new Set(notes.map(n=>n.channel)).size};
}

async function loadMidi(url,sequence) {
  try {
    let song=midiCache.get(url);
    if (!song) {
      const res=await fetch("./"+url);
      if (!res.ok) throw Error("MIDI introuvable ("+res.status+")");
      const buffer=await res.arrayBuffer();
      song={...parseMidi(buffer),buffer};
      midiCache.set(url,song);
    }
    if (sequence!==docSequence) return;
    currentMidi=song;
    playback.position=0;
    playback.needsSeek=true;
    $("playBtn").disabled=false;
    $("midiInfo").textContent=song.notes.length+" notes · "+song.channels+" partie"+(song.channels>1?"s":"")+" · MIDI format "+song.format;
    $("totalTime").textContent=formatTime(song.duration);
    $("currentTime").textContent="0:00";
    $("seek").value="0";
    drawRoll();
  } catch (err) {
    if (sequence!==docSequence) return;
    $("playerAvailable").hidden=true;
    $("playerUnavailable").hidden=false;
    $("noMidiReason").textContent="Le fichier existe, mais sa lecture a échoué : "+err.message;
    $("playerTag").textContent="Lecture indisponible";
  }
}

function initializeAudio() {
  if (playback.context) return;
  const AudioContext=window.AudioContext||window.webkitAudioContext;
  if (!AudioContext) throw Error("Le navigateur ne prend pas en charge Web Audio.");
  const context=new AudioContext();
  const compressor=context.createDynamicsCompressor();
  compressor.threshold.value=-17;compressor.knee.value=15;compressor.ratio.value=3;
  const master=context.createGain();
  master.gain.value=Number($("volume").value)/100;
  master.connect(compressor);compressor.connect(context.destination);
  playback.context=context;
  playback.master=master;
}

function getGMPlayer() {
  if (!playback.enginePromise) {
    playback.enginePromise=import("./gm-player.js")
      .then(({createGMPlayer})=>createGMPlayer(playback.context,playback.master,finishPlayback))
      .then(engine=>playback.engine=engine)
      .catch(error=>{playback.enginePromise=null;throw error;});
  }
  return playback.enginePromise;
}
function currentPosition() {
  if (!currentMidi) return 0;
  const position=playback.playing ? playback.engine.position : playback.position;
  return Math.max(0,Math.min(currentMidi.duration,position));
}
function setTransport() {
  $("playBtn").disabled=!currentMidi || playback.loading;
  $("playIcon").textContent=playback.playing ? "Ⅱ" : playback.loading ? "…" : "▶";
  $("playBtn").setAttribute("aria-label",playback.playing ? "Mettre en pause le MIDI" :
    playback.loading ? "Chargement des sons General MIDI" : "Jouer le MIDI");
  $("audioStatus").textContent=playback.loading ? "Préparation de la lecture…" :
    playback.engine ? "GeneralUser GS · instruments échantillonnés" : "Sons General MIDI chargés à la première écoute.";
}
function pausePlayback() {
  ++playback.request; // Invalidate any pending Play (Stop, course change, or backgrounding).
  playback.loading=false;
  if (playback.playing) {
    playback.position=currentPosition();
    playback.playing=false;
    cancelAnimationFrame(playback.raf);
    playback.raf=null;
  }
  playback.engine?.pause();
  setTransport();
  updateTime();
}
function stopPlayback() {
  pausePlayback();
  playback.position=0;
  playback.needsSeek=true;
  updateTime();
}
function finishPlayback() {
  if (!playback.playing || !currentMidi) return;
  playback.playing=false;
  playback.position=currentMidi.duration;
  playback.needsSeek=true;
  cancelAnimationFrame(playback.raf);
  playback.raf=null;
  setTransport();
  updateTime();
}
function updateTime() {
  const position=currentPosition(),duration=currentMidi?currentMidi.duration:0;
  $("currentTime").textContent=formatTime(position);
  $("totalTime").textContent=formatTime(duration);
  $("seek").value=duration?String(Math.max(0,Math.min(1000,Math.round(position/duration*1000)))):"0";
  drawRoll();
}
function animation() {
  if (!playback.playing) return;
  updateTime();
  playback.raf=requestAnimationFrame(animation);
}
async function startPlayback() {
  const song=currentMidi;
  if (!song || playback.playing || playback.loading) return;
  for (const audio of $("audioTracks").querySelectorAll("audio")) audio.pause();
  const request=++playback.request;
  playback.loading=true;
  setTransport();
  notice("");
  try {
    initializeAudio();
    // Resume in the click handler, before awaiting the SoundFont or the worklet (iOS).
    await playback.context.resume();
    if (request!==playback.request) return;
    const engine=await getGMPlayer();
    if (request!==playback.request) return;
    await engine.load(song);
    if (request!==playback.request) return;
    if (playback.position>=song.duration) {
      playback.position=0;
      playback.needsSeek=true;
    }
    engine.speed(Number($("speed").value)||1);
    engine.play(playback.needsSeek ? playback.position : undefined);
    playback.needsSeek=false;
    playback.playing=true;
    playback.raf=requestAnimationFrame(animation);
  } catch (error) {
    if (request===playback.request) notice("Impossible de charger le son General MIDI : "+error.message+" Tu peux réessayer ou télécharger le fichier MIDI.");
  } finally {
    if (request===playback.request) {
      playback.loading=false;
      setTransport();
    }
  }
}
function seekTo(position) {
  if (!currentMidi) return;
  playback.position=Math.max(0,Math.min(currentMidi.duration,position));
  if (playback.playing && playback.position<currentMidi.duration) {
    playback.engine.seek(playback.position);
    return; // The worklet reports the new position asynchronously.
  } else if (playback.playing) {
    pausePlayback();
    playback.position=currentMidi.duration;
    playback.needsSeek=true;
  } else {
    playback.needsSeek=true;
  }
  updateTime();
}
function drawRoll() {
  const canvas=$("pianoRoll"),rect=canvas.getBoundingClientRect();
  if (!rect.width || !rect.height) return;
  const dpr=Math.min(window.devicePixelRatio||1,2),w=rect.width,h=rect.height;
  const pixelWidth=Math.round(w*dpr),pixelHeight=Math.round(h*dpr);
  if (canvas.width!==pixelWidth || canvas.height!==pixelHeight) {canvas.width=pixelWidth;canvas.height=pixelHeight;}
  const c=canvas.getContext("2d");c.setTransform(dpr,0,0,dpr,0,0);
  c.fillStyle="#151e34";c.fillRect(0,0,w,h);
  const left=18,right=w-16,top=29,bottom=h-19;
  const rollH=bottom-top;
  const song=currentMidi;
  if (!song || !song.notes.length) {
    c.font="12px sans-serif";c.fillStyle="#78869f";
    c.textAlign="center";c.fillText("Sélectionne un exemple MIDI pour afficher ses notes",w/2,h/2);return;
  }
  const pitches=song.notes.map(n=>n.pitch);
  const minP=Math.max(0,Math.min(...pitches)-2),maxP=Math.min(127,Math.max(...pitches)+2),range=Math.max(8,maxP-minP+1);
  const rowH=rollH/range,duration=Math.max(.5,song.duration);
  const x=(t)=>left+(t/duration)*(right-left);
  for (let note=minP;note<=maxP;note++) {
    if ([1,3,6,8,10].includes(note%12)) {
      c.fillStyle="#ffffff06";
      const y=top+(maxP-note)*rowH;
      c.fillRect(left,y,right-left,rowH);
    }
  }
  c.strokeStyle="#ffffff12";c.lineWidth=1;
  for (let s=0;s<=duration;s+=duration>65?10:duration>25?5:2) {
    const at=x(s);
    c.beginPath();c.moveTo(at,top);c.lineTo(at,bottom);c.stroke();
    c.font="9px sans-serif";c.fillStyle="#8a98b3";c.textAlign="center";c.fillText(formatTime(s),at,h-6);
  }
  for (const n of song.notes) {
    const at=x(n.start),end=x(n.end);
    const y=top+(maxP-n.pitch)*rowH+Math.min(1,rowH*.1);
    c.fillStyle=COLORS[n.channel%COLORS.length];
    c.globalAlpha=.5+Math.min(.45,n.velocity/200);
    c.fillRect(at,y,Math.max(2,end-at-.4),Math.max(2,rowH-.8));
  }
  c.globalAlpha=1;
  const playX=x(currentPosition());
  c.strokeStyle="#fff";c.lineWidth=1.5;
  c.beginPath();c.moveTo(playX,top-3);c.lineTo(playX,bottom);c.stroke();
  c.fillStyle="#fff";c.beginPath();c.moveTo(playX-4,top-5);c.lineTo(playX+4,top-5);c.lineTo(playX,top+1);c.closePath();c.fill();
}

async function boot() {
  try {
    const response=await fetch("./catalog.json");
    if (!response.ok) throw Error("Impossible de charger le catalogue (HTTP "+response.status+")");
    const data=await response.json();
    catalog=Array.isArray(data.courses)?data.courses:[];
    const sum=data.summary||{};
    $("metricCourses").textContent=catalog.length;
    $("metricMidi").textContent=catalog.filter(r=>r.midi).length;
    $("metricReviewed").textContent=(sum.detailed_with_midi||0)+(sum.reviewed_with_limitation_no_midi||0);
    catalog.sort((a,b)=>{
      const priority=(r)=>r.midi?0:r.review_state==="first_scope_assessed_without_midi"?1:r.review_state==="not_yet_assessed"?2:3;
      return priority(a)-priority(b) || a.institution.localeCompare(b.institution) || a.code.localeCompare(b.code,undefined,{numeric:true});
    });
    const wanted=courseFromLink(new URLSearchParams(window.location.search).get("cours"));
    if (wanted) {
      // A browser can restore filter fields on reload. The direct link wins.
      $("search").value="";
      $("school").value="all";
      $("status").value="all";
      showCourse(wanted.id,false);
    }
    drawCourses();
    if (wanted) {
      requestAnimationFrame(() => {
        if (current?.id !== wanted.id) return;
        const list = $("courseList");
        const selected = list.querySelector('[aria-current="true"]');
        if (!selected) return;
        if (window.matchMedia("(max-width: 740px)").matches) {
          list.scrollLeft += selected.getBoundingClientRect().left - list.getBoundingClientRect().left;
          if (!new URLSearchParams(window.location.search).has("etude")) {
            $("detail").scrollIntoView({block:"start",behavior:"instant"});
          }
        } else {
          list.scrollTop += selected.getBoundingClientRect().top - list.getBoundingClientRect().top;
        }
      });
    }
  } catch (error) {
    $("resultCount").textContent="Catalogue indisponible";
    $("detail").hidden=true;
    notice("Le site n'a pas pu charger ses données : "+error.message+
      ". Si tu ouvres index.html directement, utilise la version publiée par GitHub Pages.");
  }
}
$("search").addEventListener("input",drawCourses);
$("school").addEventListener("change",drawCourses);
$("status").addEventListener("change",drawCourses);
$("resetFilters").addEventListener("click",()=>{$("search").value="";$("school").value="all";$("status").value="all";drawCourses();});
$("tabDescription").addEventListener("click",()=>switchTab("description"));
$("tabApplication").addEventListener("click",()=>switchTab("application"));
$("playBtn").addEventListener("click",()=>playback.playing?pausePlayback():startPlayback());
$("stopBtn").addEventListener("click",stopPlayback);
$("seek").addEventListener("change",e=>seekTo(Number(e.target.value)/1000*(currentMidi?currentMidi.duration:0)));
$("volume").addEventListener("input",e=>{if (playback.master) playback.master.gain.value=Number(e.target.value)/100;});
$("speed").addEventListener("change",()=>{if(playback.engine)playback.engine.speed(Number($("speed").value)||1);});
window.addEventListener("resize",drawRoll);
document.addEventListener("visibilitychange",()=>{if(document.hidden)pausePlayback();});
document.addEventListener("keydown",e=>{
  if(e.key==="/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)){e.preventDefault();$("search").focus();}
});
boot();
