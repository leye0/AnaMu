"""Regression tests against scientific overclaims, without downloading MIDI."""

import copy
import unittest

from anamu.research_contracts import (ResearchContractError, check_experiment,
                                      check_registered_experiment, load_catalog,
                                      validate_catalog)


class ResearchEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def proposal(self, source="PIAST_AT", target="mood_tags", **changes):
        proposal = copy.deepcopy(self.catalog["experiments"]["piast_tonal_motion"])
        proposal["source"] = source
        proposal["target"] = target
        proposal.update(changes)
        return proposal

    def reject(self, spec, pattern):
        with self.assertRaisesRegex(ResearchContractError, pattern):
            check_experiment("proposal", spec, self.catalog)

    def test_real_catalog_and_entrypoints(self):
        validate_catalog(self.catalog)
        for name in self.catalog["experiments"]:
            check_registered_experiment(name)

    def test_piast_global_tags_are_not_temporal_emotion_labels(self):
        self.reject(self.proposal(requires_temporal_human_labels=True),
                    "no time-resolved human labels")

    def test_vgmidi_va_does_not_supply_mysterious_tag(self):
        self.reject(self.proposal(source="VGMIDI", target="mood_tags"),
                    "does not expose human target")

    def test_emopia_quadrant_is_not_a_four_vote_soft_label(self):
        self.reject(self.proposal(source="EMOPIA", target="va_quadrant",
                                  requires_individual_votes=True),
                    "does not expose independently usable votes")

    def test_percepiano_tags_are_not_piast_moods(self):
        self.reject(self.proposal(source="PERCEPIANO", target="mood_tags"),
                    "does not expose human target")

    def test_inappropriate_grouping_is_refused(self):
        self.reject(self.proposal(split_group="clip"), "split must group by")

    def test_old_piast_cannot_be_called_independent_confirmation(self):
        self.reject(self.proposal(status="confirmatory",
                                  independent_test_preregistered=True),
                    "already examined test data")

    def test_new_data_also_needs_frozen_confirmatory_protocol(self):
        self.reject(self.proposal(status="confirmatory", previously_examined=False),
                    "independently frozen selection")

    def test_cannot_call_idyom_import_original_engine_execution(self):
        self.reject(self.proposal(methods=[{
            "id": "idyom_original", "claim": "published_engine_executed"
        }]), "original engine not executed")

    def test_cannot_call_own_proxy_published_algorithm(self):
        self.reject(self.proposal(methods=[{
            "id": "tonal_motion_proxy", "claim": "published_engine_executed"
        }]), "original engine not executed")

    def test_no_new_affective_claim_inferred_from_temporal_features(self):
        self.reject(self.proposal(claim_scope="temporal_valence_arousal_association"),
                    "incompatible")

    def test_confirmatory_gate_passes_only_compatible_fresh_protocol(self):
        spec = self.proposal(status="confirmatory", previously_examined=False,
                             independent_test_preregistered=True)
        check_experiment("new_frozen_study", spec, self.catalog)

    def test_catalog_rejects_missing_source_contract(self):
        broken = copy.deepcopy(self.catalog)
        del broken["sources"]["PIAST_AT"]["independent_group"]
        with self.assertRaisesRegex(ResearchContractError, "missing independent_group"):
            validate_catalog(broken)

    def test_duplicate_method_not_allowed(self):
        methods = self.proposal()["methods"]
        self.reject(self.proposal(methods=methods + methods), "duplicate method")

    def test_cudlun_exposes_human_note_expectancy_not_emotions(self):
        spec = copy.deepcopy(self.catalog["experiments"]["cudlun_human_expectancy"])
        check_experiment("expectancy", spec, self.catalog)
        spec["target"] = "mood_tags"
        self.reject(spec, "does not expose human target")

    def test_cudlun_cannot_claim_individual_listener_votes(self):
        spec = copy.deepcopy(self.catalog["experiments"]["cudlun_human_expectancy"])
        spec["requires_individual_votes"] = True
        self.reject(spec, "does not expose independently usable votes")

    def test_cudlun_cannot_be_called_temporal_ground_truth(self):
        spec = copy.deepcopy(self.catalog["experiments"]["cudlun_human_expectancy"])
        spec["requires_temporal_human_labels"] = True
        self.reject(spec, "no time-resolved human labels")

    def test_cudlun_proxy_cannot_claim_original_narmour_implementation(self):
        spec = copy.deepcopy(self.catalog["experiments"]["cudlun_human_expectancy"])
        spec["methods"] = [{"id": "cuddy_narmour_proxy",
                            "claim": "published_engine_executed"}]
        self.reject(spec, "original engine not executed")


if __name__ == "__main__":
    unittest.main()
