import io
import math
import unittest

from anamu.expectation import VariableOrderExpectancy
from anamu.midi_views import extract_monophonic_candidates


class ExpectationTests(unittest.TestCase):
    def test_probability_distribution_is_normalized_and_finite(self):
        model = VariableOrderExpectancy(max_order=2).fit([[0, 2, 0, 2] * 10,
                                                          [1, 3, 1, 3] * 10])
        for context in ([], [0], [0, 2], [99, 99]):
            distribution = model.distribution(context)
            self.assertAlmostEqual(sum(distribution.values()), 1.0, places=12)
            self.assertTrue(all(0 < p < 1 for p in distribution.values()))

    def test_expected_continuation_has_less_surprisal(self):
        model = VariableOrderExpectancy(max_order=2).fit([[0, 2] * 40,
                                                          [1, 3] * 40])
        expected = model.probability(2, [0])
        unexpected = model.probability(3, [0])
        self.assertGreater(expected, unexpected)
        self.assertLess(-math.log2(expected), -math.log2(unexpected))

    def test_evaluation_does_not_learn_test_sequence(self):
        model = VariableOrderExpectancy().fit([[0, 2, 4, 0, 2, 4]])
        original = model.probability(4, [0, 2])
        evaluations = model.evaluate([4, 4, 4])
        self.assertEqual(len(evaluations), 3)
        self.assertEqual(model.probability(4, [0, 2]), original)
        self.assertEqual(evaluations[0].context_length, 0)

    def test_unknown_event_has_nonzero_probability(self):
        model = VariableOrderExpectancy().fit([[0, 1, 2]])
        self.assertGreater(model.probability(777, [0, 1]), 0)
        self.assertAlmostEqual(model.probability(777), model.distribution()["<UNSEEN>"])

    def test_invalid_or_unfitted_model(self):
        with self.assertRaises(ValueError):
            VariableOrderExpectancy(smoothing=0)
        with self.assertRaises(ValueError):
            VariableOrderExpectancy().fit([])
        with self.assertRaises(RuntimeError):
            VariableOrderExpectancy().evaluate([1])
        with self.assertRaises(ValueError):
            VariableOrderExpectancy().fit([["<UNSEEN>"]])


class MidiViewsTests(unittest.TestCase):
    def _midi(self, pitches, overlap=False):
        import mido
        score = mido.MidiFile(type=1, ticks_per_beat=480)
        track = mido.MidiTrack()
        score.tracks.append(track)
        if overlap:
            for pitch in pitches:
                track.append(mido.Message("note_on", channel=0, note=pitch, velocity=80, time=0))
            for pitch in pitches:
                track.append(mido.Message("note_off", channel=0, note=pitch, velocity=0, time=120))
        else:
            for pitch in pitches:
                track.append(mido.Message("note_on", channel=0, note=pitch, velocity=80, time=120))
                track.append(mido.Message("note_off", channel=0, note=pitch, velocity=0, time=120))
        stream = io.BytesIO()
        score.save(file=stream)
        return stream.getvalue()

    def test_intervals_and_beats_are_transposition_invariant(self):
        first = extract_monophonic_candidates(self._midi([60, 64, 67]))
        second = extract_monophonic_candidates(self._midi([72, 76, 79]))
        a, b = first["candidates"][0], second["candidates"][0]
        self.assertEqual(a["intervals"], (4, 3))
        self.assertEqual(a["intervals"], b["intervals"])
        self.assertEqual(a["notes"][0]["start_beats"], 0.25)
        self.assertFalse(first["candidates_are_verified_melodies"])

    def test_polyphony_is_rejected_not_mislabelled_as_melody(self):
        result = extract_monophonic_candidates(self._midi([60, 64, 67], overlap=True))
        self.assertFalse(result["candidates"])
        self.assertIn("polyphonic_or_overlapping_notes", result["rejected_parts"][0]["reasons"])

    def test_drum_channel_is_excluded(self):
        import mido
        score = mido.MidiFile()
        track = mido.MidiTrack()
        score.tracks.append(track)
        for pitch in [36, 38, 42]:
            track.append(mido.Message("note_on", channel=9, note=pitch, velocity=70, time=100))
            track.append(mido.Message("note_off", channel=9, note=pitch, velocity=0, time=100))
        buffer = io.BytesIO()
        score.save(file=buffer)
        self.assertEqual(extract_monophonic_candidates(buffer.getvalue())["candidates"], [])

    def test_direct_midi_to_expected_intervals_without_audio(self):
        reference = extract_monophonic_candidates(self._midi([60, 62, 64, 66, 68]))
        evaluation = extract_monophonic_candidates(self._midi([72, 74, 76, 78]))
        model = VariableOrderExpectancy(max_order=2).fit([
            reference["candidates"][0]["intervals"]
        ])
        events = model.evaluate(evaluation["candidates"][0]["intervals"])
        self.assertEqual(len(events), 3)
        self.assertTrue(all(event.surprisal_bits >= 0 for event in events))
        self.assertTrue(all(math.isfinite(event.entropy_bits_before) for event in events))

    def test_incomplete_notes_remain_rejected(self):
        import mido
        score = mido.MidiFile()
        track = mido.MidiTrack()
        score.tracks.append(track)
        for pitch in [60, 62, 64]:
            track.append(mido.Message("note_on", channel=0, note=pitch, time=120))
            track.append(mido.Message("note_off", channel=0, note=pitch, time=120))
        track.append(mido.Message("note_on", channel=0, note=67, time=120))
        buffer = io.BytesIO()
        score.save(file=buffer)
        result = extract_monophonic_candidates(buffer.getvalue())
        self.assertFalse(result["candidates"])
        self.assertIn("unclosed_note", result["rejected_parts"][0]["reasons"])


if __name__ == "__main__":
    unittest.main()
