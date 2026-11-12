/* AnaMu Pages — standalone MIDI browser player, no library or service required. */
"use strict";

const $ = (id) => document.getElementById(id);
const SCHOOLS = {udem:"Université de Montréal",mcgill:"McGill",berklee:"Berklee"};
const SHORT = {udem:"UdeM",mcgill:"McGill",berklee:"Berklee"};
const STATES = {
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
  context: null, master: null, compressor: null, noise: null,
  playing: false, timer: null, raf: null,
  position: 0, originSong: 0, originAudio: 0, next: 0,
  rate: 1, voices: [], activeUrl: ""
};

function normalize(text) {
  return String(text || "").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
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
  const response = await fetch("./" + entry.detail);
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
async function showCourse(id, historyUpdate) {
  const entry = catalog.find((c) => c.id === id);
  if (!entry) return;
  if (playback.playing || playback.position || (current && current.id !== entry.id)) stopPlayback();
  current = entry;
  const seq = ++docSequence;
  if (historyUpdate) {
    const url = new URL(window.location.href);
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
  setTag(entry.coverage==="usable_first_pass"?"Contenu recensé":entry.coverage==="partial"?"Contenu partiel":"Choix à préciser","violet");
  if (entry.non_algorithmic===true) setTag("Non algorithmique (musique)","alert");
  else if (entry.non_algorithmic===false) setTag("Application algorithmique possible","midi");
  for (const t of entry.algorithmic_tags.slice(0,4)) setTag(t.replace(/_/g," "),"");
  $("descriptionContent").innerHTML = '<p class="missing-description">Chargement de la description…</p>';
  $("applicationContent").innerHTML = '<p class="missing-description">Chargement de l’analyse…</p>';
  $("playerAvailable").hidden = !entry.midi;
  $("playerUnavailable").hidden = !!entry.midi;
  $("playerTag").textContent = entry.midi ? "MIDI original" : "Pas de MIDI";
  $("midiInfo").textContent = "Chargement…";
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
      song=parseMidi(await res.arrayBuffer());
      midiCache.set(url,song);
    }
    if (sequence!==docSequence) return;
    currentMidi=song;
    playback.activeUrl=url;
    playback.position=0;
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
  const sample=context.createBuffer(1,context.sampleRate,context.sampleRate);
  const channel=sample.getChannelData(0);
  for (let i=0;i<channel.length;i++) channel[i]=(Math.random()*2)-1;
  playback.context=context;playback.master=master;playback.compressor=compressor;playback.noise=sample;
}

function voice(note,when,duration) {
  const ctx=playback.context;
  if (!ctx || duration<=0) return;
  const channel=note.channel,program=note.program;
  const amp=Math.max(.02,(note.velocity/127)*.115);
  if (channel===9) {
    const gain=ctx.createGain();gain.connect(playback.master);
    const isKick=note.pitch===35||note.pitch===36;
    const isHat=note.pitch===42||note.pitch===44||note.pitch===46;
    const length=Math.min(duration,isHat?.095:.18);
    if (isKick) {
      const osc=ctx.createOscillator();osc.type="sine";
      osc.frequency.setValueAtTime(125,when);
      osc.frequency.exponentialRampToValueAtTime(47,when+Math.max(.06,length));
      gain.gain.setValueAtTime(amp*1.4,when);
      gain.gain.exponentialRampToValueAtTime(.0001,when+length+.03);
      osc.connect(gain);osc.start(when);osc.stop(when+length+.05);
      playback.voices.push(osc);
    } else {
      const noise=ctx.createBufferSource();noise.buffer=playback.noise;
      const filter=ctx.createBiquadFilter();
      filter.type=isHat?"highpass":"bandpass";filter.frequency.value=isHat?6000:1650;
      gain.gain.setValueAtTime(amp,when);
      gain.gain.exponentialRampToValueAtTime(.0001,when+length+.03);
      noise.connect(filter);filter.connect(gain);
      noise.start(when);noise.stop(when+length+.05);
      playback.voices.push(noise);
    }
    return;
  }
  const isPiano=program<=7 || program===11;
  const isStrings=(program>=40 && program<=51)||program===52;
  const isWind=program>=64&&program<=79;
  const isBass=program>=32&&program<=39;
  const isSynth=program>=80;
  const osc=ctx.createOscillator();
  osc.type=isStrings?"sawtooth":isWind?"sine":isSynth?"square":isBass?"sine":isPiano?"triangle":"triangle";
  osc.frequency.value=440*Math.pow(2,(note.pitch-69)/12);
  const filter=ctx.createBiquadFilter();
  filter.type="lowpass";filter.frequency.value=isStrings?2600:isSynth?1850:isPiano?4400:6200;
  const gain=ctx.createGain();
  const start=Math.max(when,ctx.currentTime);
  const attack=Math.min(isStrings?.065:isWind?.026:.007,Math.max(.003,duration/4));
  const release=isStrings?.19:isPiano?.17:.1;
  const end=start+duration;
  gain.gain.setValueAtTime(.0001,start);
  gain.gain.exponentialRampToValueAtTime(amp,start+attack);
  if (isPiano) gain.gain.setTargetAtTime(amp*.42,start+attack,Math.max(.08,duration*.28));
  else gain.gain.setTargetAtTime(amp*.78,start+attack,.11);
  gain.gain.setTargetAtTime(.0001,end,Math.max(.025,release/4));
  osc.connect(filter);filter.connect(gain);gain.connect(playback.master);
  osc.start(start);osc.stop(end+release);
  playback.voices.push(osc);
}
function currentPosition() {
  if (!currentMidi) return 0;
  if (!playback.playing) return playback.position;
  return Math.min(currentMidi.duration, Math.max(0,playback.originSong+
    (playback.context.currentTime-playback.originAudio)*playback.rate));
}
function stopSources() {
  for (const source of playback.voices) {
    try { source.stop(); } catch (_err) { /* already stopped */ }
  }
  playback.voices=[];
}
function pausePlayback() {
  if (!playback.playing) return;
  playback.position=currentPosition();
  playback.playing=false;
  clearInterval(playback.timer);playback.timer=null;
  cancelAnimationFrame(playback.raf);playback.raf=null;
  stopSources();
  $("playIcon").textContent="▶";
  $("playBtn").setAttribute("aria-label","Jouer le MIDI");
  updateTime();
}
function stopPlayback() {
  pausePlayback();
  playback.position=0;
  playback.activeUrl="";
  $("playIcon").textContent="▶";
  updateTime();
}
function updateTime() {
  const position=currentPosition(),duration=currentMidi?currentMidi.duration:0;
  $("currentTime").textContent=formatTime(position);
  $("totalTime").textContent=formatTime(duration);
  $("seek").value=duration?String(Math.max(0,Math.min(1000,Math.round(position/duration*1000)))):"0";
  drawRoll();
}
function scheduleAhead() {
  if (!currentMidi || !playback.playing) return;
  const now=playback.context.currentTime;
  const until=now+.24;
  const maxSong=playback.originSong+(until-playback.originAudio)*playback.rate;
  while (playback.next<currentMidi.notes.length && currentMidi.notes[playback.next].start<=maxSong) {
    const note=currentMidi.notes[playback.next++];
    if (note.end<=playback.originSong) continue;
    const effectiveStart=Math.max(note.start,playback.originSong);
    const at=playback.originAudio+(effectiveStart-playback.originSong)/playback.rate;
    const duration=(note.end-effectiveStart)/playback.rate;
    voice(note,at,duration);
  }
  if (currentPosition()>=currentMidi.duration) {
    pausePlayback();
    playback.position=currentMidi.duration;
    updateTime();
  }
}
function animation() {
  if (!playback.playing) return;
  updateTime();
  playback.raf=requestAnimationFrame(animation);
}
async function startPlayback() {
  if (!currentMidi || playback.playing) return;
  try {
    initializeAudio(); // Must happen in the user's click handler for iOS audio.
    await playback.context.resume();
    if (playback.position>=currentMidi.duration) playback.position=0;
    playback.rate=Number($("speed").value)||1;
    playback.originSong=playback.position;
    playback.originAudio=playback.context.currentTime+.085;
    playback.next=currentMidi.notes.findIndex(n=>n.end>playback.position);
    if (playback.next<0) playback.next=currentMidi.notes.length;
    playback.playing=true;
    $("playIcon").textContent="Ⅱ";
    $("playBtn").setAttribute("aria-label","Mettre en pause le MIDI");
    scheduleAhead();
    playback.timer=setInterval(scheduleAhead,55);
    playback.raf=requestAnimationFrame(animation);
  } catch(err) {
    notice("Impossible d'activer le synthétiseur du navigateur : "+err.message);
  }
}
function seekTo(position) {
  const resume=playback.playing;
  pausePlayback();
  playback.position=Math.max(0,Math.min(currentMidi?currentMidi.duration:0,position));
  updateTime();
  if (resume) startPlayback();
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
    drawCourses();
    const wanted=new URLSearchParams(window.location.search).get("cours");
    if (wanted && catalog.some((c) => c.id === wanted)) showCourse(wanted,false);
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
$("speed").addEventListener("change",()=>{const was=playback.playing;pausePlayback();playback.rate=Number($("speed").value)||1;if(was)startPlayback();});
window.addEventListener("resize",drawRoll);
document.addEventListener("visibilitychange",()=>{if(document.hidden)pausePlayback();});
document.addEventListener("keydown",e=>{
  if(e.key==="/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)){e.preventDefault();$("search").focus();}
});
boot();
