import importlib.util
import io
import unittest
import zipfile

from scripts.audit_xmidi_instruments import (
    choose_samples, family, inspect_midi, is_eligible, read_midi_one_range, summarize,
)


def midi_info(label, genre, idx, body=b"MThd" + b"0" * 300):
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w", zipfile.ZIP_DEFLATED) as out:
        out.writestr(f"XMIDI_{label}_{genre}_{idx:08d}.midi", body)
    raw.seek(0)
    return raw


class InstrumentAuditTests(unittest.TestCase):
    def test_instrument_families(self):
        self.assertEqual(family(0, 0), "piano")
        self.assertEqual(family(24, 1), "guitar")
        self.assertEqual(family(32, 2), "bass")
        self.assertEqual(family(0, 9), "drums")

    def test_read_verified_midi_using_single_range(self):
        raw = midi_info("happy", "rock", 1)
        data = raw.getvalue()
        with zipfile.ZipFile(raw) as z:
            info = z.infolist()[0]
            remote = type("FakeRemote", (), {"total_size": len(data),
                                             "calls": [],
                                             "_get_range": lambda self, a, b: (
                                                 self.calls.append((a, b)) or data[a:b + 1])})()
            self.assertEqual(read_midi_one_range(remote, info), b"MThd" + b"0" * 300)
            self.assertEqual(len(remote.calls), 1)

    def test_deterministic_non_overlapping_sample_strata(self):
        raw = io.BytesIO()
        with zipfile.ZipFile(raw, "w", zipfile.ZIP_DEFLATED) as z:
            for i in range(250):
                z.writestr(f"XMIDI_happy_rock_{i:08d}.midi", b"MThd" + b"0" * 300)
            for i in range(250, 380):
                z.writestr(f"XMIDI_sad_classical_{i:08d}.midi", b"MThd" + b"0" * 300)
        with zipfile.ZipFile(raw) as z:
            selected, stats = choose_samples(z.infolist())
            a = selected["general_random"]
            b = selected["pop_rock_targeted"]
            self.assertEqual((len(a), len(b)), (100, 100))
            self.assertFalse({x.filename for x in a} & {x.filename for x in b})
            self.assertTrue(all("rock" in x.filename for x in b))
            self.assertEqual(stats["eligible_pop_rock_grunge"], 250)
            self.assertEqual([x.filename for x in a],
                             [x.filename for x in choose_samples(z.infolist())[0]["general_random"]])

    def test_report_denominators_and_trio_counts(self):
        row = {"piano_only": False, "drums_only": False, "guitar_bass_drums_present": True,
               "guitar_bass_drums_sustained": False, "note_bearing_tracks": 3,
               "note_bearing_parts": 3, "total_notes": 90, "duration_seconds": 10.0,
               "notes_by_family": {"guitar": 30, "bass": 30, "drums": 30}}
        report = summarize([row], {})
        self.assertEqual(report["flag_percent_of_parsed"]["guitar_bass_drums_present"], 100.0)
        self.assertEqual(report["files_with_family"], {"guitar": 1, "bass": 1, "drums": 1})


@unittest.skipUnless(importlib.util.find_spec("mido") is not None, "mido optional in other workflows")
class MidiNoteTests(unittest.TestCase):
    def test_active_guitar_bass_drums_not_merely_declared(self):
        import mido
        midi = mido.MidiFile(type=1)
        for channel, program in ((0, 25), (1, 34), (9, None)):
            track = mido.MidiTrack()
            midi.tracks.append(track)
            if program is not None:
                track.append(mido.Message("program_change", channel=channel,
                                          program=program, time=0))
            for i in range(20):
                track.append(mido.Message("note_on", channel=channel, note=60,
                                          velocity=90, time=120))
                track.append(mido.Message("note_off", channel=channel, note=60,
                                          velocity=0, time=120))
        buf = io.BytesIO()
        midi.save(file=buf)
        report = inspect_midi(buf.getvalue())
        self.assertEqual(report["note_bearing_tracks"], 3)
        self.assertEqual(report["notes_by_family"], {"guitar": 20, "bass": 20, "drums": 20})
        self.assertTrue(report["guitar_bass_drums_present"])
        self.assertTrue(report["guitar_bass_drums_sustained"])

    def test_piano_reduction_is_not_full_band(self):
        import mido
        midi = mido.MidiFile()
        track = mido.MidiTrack()
        midi.tracks.append(track)
        track.append(mido.Message("program_change", channel=0, program=0))
        track.append(mido.Message("note_on", channel=0, note=60, velocity=80))
        buf = io.BytesIO()
        midi.save(file=buf)
        report = inspect_midi(buf.getvalue())
        self.assertTrue(report["piano_only"])
        self.assertFalse(report["guitar_bass_drums_present"])


if __name__ == "__main__":
    unittest.main()
