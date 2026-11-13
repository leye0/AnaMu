// The library and its AudioWorklet must use the same version.
const SPESSA = "https://cdn.jsdelivr.net/npm/spessasynth_lib@4.4.8";
const BANK = "https://cdn.jsdelivr.net/gh/spessasus/SpessaSynth@d7b0657606602bb2072b8e28900271f1762409bb/soundfonts/GeneralUserGS.sf3";
const BANK_INTEGRITY = "sha384-DOXK/RqJ2TJwih8ArNBdZaATb26azpizj4W2CDnBc0JwHTH61T9MHZqqS0k71eYm";

async function getSoundBank() {
  const response = await fetch(BANK, {integrity: BANK_INTEGRITY, signal: AbortSignal.timeout(45000)});
  if (!response.ok) throw new Error("Banque de sons introuvable (HTTP " + response.status + ").");
  return response.arrayBuffer();
}

export async function createGMPlayer(context, output, onEnd) {
  if (!context.audioWorklet) throw new Error("La lecture General MIDI exige Web Audio sur une page HTTPS.");
  const [{Sequencer, WorkletSynthesizer}, bank] = await Promise.all([
    import(SPESSA + "/+esm"),
    getSoundBank(),
    context.audioWorklet.addModule(SPESSA + "/dist/spessasynth_processor.min.js")
  ]);
  const synth = new WorkletSynthesizer(context);
  // Mute release and reverb tails on an explicit Pause/Stop, independently of volume.
  const transportGain = context.createGain();
  transportGain.gain.value = 0;
  synth.connect(transportGain);
  transportGain.connect(output);
  try {
    await synth.isReady;
    await synth.soundBankManager.addSoundBank(bank, "GeneralUser GS");
  } catch (error) {
    transportGain.disconnect();
    synth.destroy();
    throw error;
  }
  const seq = new Sequencer(synth, {skipToFirstNoteOn:false});
  seq.eventHandler.addEvent("songEnded", "anamu", onEnd);
  let loaded = null;
  let queue = Promise.resolve();
  const mute = (value) => {
    transportGain.gain.cancelScheduledValues(context.currentTime);
    transportGain.gain.setTargetAtTime(value ? 0 : 1, context.currentTime, .004);
  };

  return {
    load(song) {
      const request = queue.then(() => {
        if (loaded === song) return;
        loaded = null;
        return new Promise((resolve, reject) => {
          const cleanup = () => {
            clearTimeout(timer);
            seq.eventHandler.removeEvent("songChange", "anamu-load");
            seq.eventHandler.removeEvent("midiError", "anamu-load");
          };
          const fail = (error) => { cleanup(); reject(error); };
          const timer = setTimeout(() => fail(new Error("Le lecteur n’a pas pu préparer le fichier MIDI.")), 15000);
          seq.eventHandler.addEvent("songChange", "anamu-load", () => {
            cleanup();
            loaded = song;
            resolve();
          });
          seq.eventHandler.addEvent("midiError", "anamu-load", fail);
          try {
            seq.loadNewSongList([{binary:song.buffer}]);
          } catch (error) {
            fail(error);
          }
        });
      });
      queue = request.catch(() => {});
      return request;
    },
    get position() { return seq.currentTime; },
    play(position) {
      if (position !== undefined) seq.currentTime = position;
      mute(false);
      seq.play();
    },
    pause() { mute(true); seq.pause(); synth.stopAll(true); },
    seek(position) { seq.currentTime = position; },
    speed(rate) { seq.playbackRate = rate; }
  };
}
