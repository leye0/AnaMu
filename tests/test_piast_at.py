"""PIAST-AT's human-label semantics, disjoint splits and MIDI-only inputs."""

import tempfile
import unittest
import hashlib
from pathlib import Path

from anamu.piast_at import (MOOD_LABELS, PIASTClip, assigned_split,
                            load_annotations, tag_popularity)
from scripts.piast_at_benchmark import score_labels, summarize_measures


class PIASTATTests(unittest.TestCase):
    def test_agreement_levels_are_not_misread_as_three_separate_ratings(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "human.csv"
            csv_path.write_text(
                "AudioFile,Agreements_3,Agreements_2,Agreements_1\n"
                'abc123,Happy,"Sad,Jazz","Dreamy,Laid-back"\n'
                'xyz456,,"Happy,Dark","Ragtime,Passionate"\n',
                encoding="utf-8")
            clips = load_annotations(csv_path)
            self.assertEqual(clips[0].mood_tags(3), frozenset({"Happy"}))
            self.assertEqual(clips[0].mood_tags(2), frozenset({"Happy", "Sad"}))
            self.assertEqual(clips[0].mood_tags(1), frozenset(
                {"Happy", "Sad", "Dreamy"}))
            self.assertEqual(clips[1].mood_tags(2), frozenset({"Happy", "Dark"}))
            counts = {x["tag"]: x for x in tag_popularity(clips)}
            self.assertEqual(counts["Happy"], {
                "tag": "Happy", "clips_with_tag": 2,
                "human_votes": 5, "majority_clips": 2})
            self.assertNotIn("Jazz", counts)

    def test_source_excerpts_remain_together(self):
        original = PIASTClip("song123_part_1", "song123_part_1.mid", "song123",
                             frozenset({"Happy"}), frozenset(), frozenset())
        repeat = PIASTClip("song123_part_2", "song123_part_2.mid", "song123",
                           frozenset({"Sad"}), frozenset(), frozenset())
        self.assertEqual(assigned_split(original), assigned_split(repeat))

    def test_deterministic_sample_does_not_bias_split(self):
        examples = [PIASTClip(f"video{i:06d}", f"video{i:06d}.mid", f"video{i:06d}",
                              frozenset(), frozenset(), frozenset())
                    for i in range(1000)]
        sampled = sorted(examples, key=lambda c: hashlib.sha256(
            f"20261108|{c.clip_id}".encode()).hexdigest())[:240]
        split = [assigned_split(clip) for clip in sampled]
        self.assertGreater(sum(s == "validation" for s in split), 10)
        self.assertGreater(sum(s == "test" for s in split), 10)

    def test_reject_unknown_or_overlapping_human_tags(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "labels.csv"
            for row in ('abc123,Joy,Happy,Sad', 'abc123,Happy,Happy,Sad'):
                with self.subTest(row=row):
                    source.write_text("AudioFile,Agreements_3,Agreements_2,Agreements_1\n"
                                      + row + "\n", encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_annotations(source)

    def test_midi_summaries_are_independent_of_annotations(self):
        a = summarize_measures([{"note_density": 2., "mean_pitch": 60.},
                                {"note_density": 4., "mean_pitch": None}])
        self.assertEqual(a["note_density__mean"], 3.)
        self.assertEqual(a["note_density__last_minus_first"], 2.)
        self.assertEqual(a["mean_pitch__observed_fraction"], .5)
        self.assertNotIn("Sad", a)

    def test_heldout_scoring_is_explicit_about_rare_moods(self):
        def record(i):
            happy = i % 2 == 0
            clip = PIASTClip(str(i), str(i) + ".mid", str(i),
                             frozenset({"Happy"}) if happy else frozenset(),
                             frozenset(), frozenset())
            return clip, {"note_density__mean": float(i % 3)}
        train = [record(i) for i in range(30)]
        test = [record(i) for i in range(30, 40)]
        scores = score_labels(train, test, ["note_density__mean"])
        self.assertEqual(scores["per_mood"]["Happy"]["evaluated_positives"], 5)
        self.assertTrue(scores["per_mood"]["Happy"]["eligible"])
        self.assertIsNone(scores["per_mood"]["Sad"]["average_precision"])
        self.assertEqual(len(MOOD_LABELS), len(scores["per_mood"]))


if __name__ == "__main__":
    unittest.main()
