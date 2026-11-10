"""Research gates for independent musical structure and expectation tasks."""

import copy
import unittest

from anamu.research_contracts import (ResearchContractError, check_experiment,
                                      check_registered_experiment, load_catalog,
                                      validate_catalog)


class ResearchEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def proposal(self, **changes):
        spec = copy.deepcopy(self.catalog["experiments"]["cudlun_human_expectancy"])
        spec.update(changes)
        return spec

    def reject(self, spec, pattern):
        with self.assertRaisesRegex(ResearchContractError, pattern):
            check_experiment("proposal", spec, self.catalog)

    def test_registered_studies_have_current_sources_and_valid_claims(self):
        validate_catalog(self.catalog)
        self.assertEqual(set(self.catalog["experiments"]), {
            "dcml_cadence_exploratory", "cudlun_human_expectancy",
            "schell_1996_external_transfer", "manzara_1992_cross_target",
            "idyom_archived_schell_probe_comparison"})
        for name in self.catalog["experiments"]:
            check_registered_experiment(name)

    def test_excluded_target_is_not_silently_accepted(self):
        self.reject(self.proposal(target="mood_tags"), "does not expose human target")

    def test_rejects_unavailable_temporal_or_individual_annotations(self):
        self.reject(self.proposal(requires_temporal_human_labels=True),
                    "no time-resolved human labels")
        self.reject(self.proposal(requires_individual_votes=True),
                    "does not expose independently usable votes")

    def test_grouping_must_be_independent(self):
        self.reject(self.proposal(split_group="individual_note"), "split must group by")

    def test_confirmation_requires_unused_data_and_frozen_protocol(self):
        self.reject(self.proposal(status="confirmatory", independent_test_preregistered=True),
                    "already examined test data")
        self.reject(self.proposal(status="confirmatory", previously_examined=False),
                    "independently frozen selection")
        check_experiment("new_protocol", self.proposal(status="confirmatory",
                         previously_examined=False, independent_test_preregistered=True),
                         self.catalog)

    def test_claim_must_match_measured_target(self):
        self.reject(self.proposal(claim_scope="musicological_cadence_detection"),
                    "incompatible")

    def test_proxy_cannot_masquerade_as_published_engine(self):
        self.reject(self.proposal(methods=[{
            "id": "cuddy_narmour_proxy", "claim": "published_engine_executed"}]),
            "original engine not executed")

    def test_unexecuted_idyom_cannot_claim_executed_original(self):
        self.reject(self.proposal(methods=[{
            "id": "idyom_original", "claim": "published_engine_executed"}]),
            "original engine not executed")

    def test_external_idyom_stays_external_and_unverified(self):
        spec = copy.deepcopy(self.catalog["experiments"]
                             ["idyom_archived_schell_probe_comparison"])
        check_experiment("external", spec, self.catalog)
        spec["methods"][1]["claim"] = "published_engine_executed"
        self.reject(spec, "original engine not executed")

    def test_source_provenance_is_required(self):
        broken = copy.deepcopy(self.catalog)
        del broken["sources"]["CUDDY_LUNNEY_1995"]["independent_group"]
        with self.assertRaisesRegex(ResearchContractError, "missing independent_group"):
            validate_catalog(broken)

    def test_duplicate_method_is_rejected(self):
        methods = self.proposal()["methods"]
        self.reject(self.proposal(methods=methods + methods), "duplicate method")

    def test_cross_target_manzara_does_not_become_probe_goodness(self):
        spec = copy.deepcopy(self.catalog["experiments"]["manzara_1992_cross_target"])
        check_experiment("realized_notes", spec, self.catalog)
        self.reject({**spec, "target": "melodic_continuation_goodness"},
                    "does not expose human target")
        self.reject({**spec, "split_group": "note"}, "split must group by")


if __name__ == "__main__":
    unittest.main()
