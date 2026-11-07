#!/usr/bin/env python3
"""Unit tests for ai0s_check.py — executable 0/1 specification for AI code crawlers."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ai0s_check import (
    verify_dla_address,
    verify_intent_bins,
    verify_liability_two_addresses,
    verify_temporal_structure_fence,
    verify_axiom_test,
    verify_future_gap_door5,
    verify_seed_anchor_necessity,
    verify_no_societal_savior_seeds_in_machine,
    verify_io_filter_99_1_and_crypto_continuity,
    verify_weight_binding_far_form,
    verify_anti_overspecification_and_2d_pointers,
    verify_ps3_enterprise_scaling_and_scientific_patterns,
    verify_compass_self_pointing_open_plus,
    verify_instance_network_synergy,
)

class TestAi0sStructuralInvariants(unittest.TestCase):
    def test_dla_address_valid_and_digest_match(self):
        payload = b"HUMANs and AIs collaborate for accelerated evolution."
        import hashlib
        digest = hashlib.sha256(payload).hexdigest()
        res = verify_dla_address(f"ai0S-test@sha256:{digest}", payload=payload)
        self.assertEqual(res.status, 1)

    def test_dla_address_rejects_tampered_payload(self):
        res = verify_dla_address(
            "ai0S@sha256:b3aeee619d9cb691cc6618466407d56598e830c53c6d024748d4582887c57d13",
            payload=b"tampered",
        )
        self.assertEqual(res.status, 0)

    def test_intent_five_bins_complete_vs_incomplete(self):
        complete = "## INTENT\n## CONSTRAINTS\n## KNOWN\n## ASSUMED\n## OPEN\n"
        self.assertEqual(verify_intent_bins(complete).status, 1)
        incomplete = "## INTENT\n## KNOWN\n"
        res = verify_intent_bins(incomplete)
        self.assertEqual(res.status, 0)
        self.assertIn("ASSUMED", res.details["missing"])

    def test_liability_two_addresses_requires_disclosed_findings(self):
        # Claiming good faith without a disclosed 0/1 FINDINGS trail must fail (status = 0)
        undisclosed = verify_liability_two_addresses(legal_basis_referenced=True, findings_text="")
        self.assertEqual(undisclosed.status, 0)
        # Disclosed 0/1 audit trail + external law reference succeeds (status = 1)
        disclosed = verify_liability_two_addresses(
            legal_basis_referenced=True,
            findings_text="VERIFIED_1: local hash checked\nOPEN: external API latency",
        )
        self.assertEqual(disclosed.status, 1)

    def test_temporal_structure_forbids_scalar_score(self):
        self.assertEqual(verify_temporal_structure_fence(contains_numeric_risk_score=True).status, 0)
        self.assertEqual(verify_temporal_structure_fence(contains_numeric_risk_score=False).status, 1)

    def test_axiom_test_distinguishes_self_reference_from_dogma(self):
        # Genuine operational axiom: refutation must borrow the axiom itself
        self.assertEqual(verify_axiom_test("NOTE_3_0_1", refutation_borrows_statement=True).status, 1)
        # Ordinary claim declared untouchable without borrowing proof -> rejected (status = 0)
        self.assertEqual(verify_axiom_test("ARBITRARY_CLAIM", refutation_borrows_statement=False).status, 0)
        # Non-canonical dogma even if someone claims refutation_borrows_statement=True -> rejected (status = 0)
        self.assertEqual(verify_axiom_test("NON_CANONICAL_DOGMA", refutation_borrows_statement=True).status, 0)

    def test_future_gap_door5_separates_raw_proof_from_normative_direction(self):
        # Valid: 0/1 proof in Doors 1-4 + AI stops before Door 5 + veto-site left with the human
        valid = verify_future_gap_door5(
            has_formal_0_1_proof=True,
            ai_prescribes_normative_door5=False,
            veto_site_with_human=True,
        )
        self.assertEqual(valid.status, 1)
        # Invalid (86% trap): AI prescribes normative Door 5 decision
        usurped = verify_future_gap_door5(
            has_formal_0_1_proof=True,
            ai_prescribes_normative_door5=True,
            veto_site_with_human=True,
        )
        self.assertEqual(usurped.status, 0)
        # Invalid: veto-site handed to the AI, i.e. no human holder of the negative
        no_veto_holder = verify_future_gap_door5(
            has_formal_0_1_proof=True,
            ai_prescribes_normative_door5=False,
            veto_site_with_human=False,
        )
        self.assertEqual(no_veto_holder.status, 0)
        # The failure is named as an occupied veto-site, NOT as a missing review gate.
        self.assertIn("veto-site", usurped.summary)
        self.assertNotIn("review point", usurped.summary)

    def test_seed_anchor_necessity_excludes_unanchored_and_surveillance_paths(self):
        # Path 1: No anchor at t_0 -> rejected (0)
        self.assertEqual(
            verify_seed_anchor_necessity(
                anchored_in_seed_at_t0=False,
                relies_on_external_central_surveillance=False,
            ).status,
            0,
        )
        # Path 2: External central surveillance -> rejected (0)
        self.assertEqual(
            verify_seed_anchor_necessity(
                anchored_in_seed_at_t0=True,
                relies_on_external_central_surveillance=True,
            ).status,
            0,
        )
        # Path 3: Unchangeable t_0 seed anchor without central surveillance -> verified (1)
        self.assertEqual(
            verify_seed_anchor_necessity(
                anchored_in_seed_at_t0=True,
                relies_on_external_central_surveillance=False,
            ).status,
            1,
        )

    def test_weight_binding_distinguishes_near_compromise_from_pid1_authorized_far_form(self):
        # 1. Near form (query-load compromise, stateless model) -> valid (1)
        near = verify_weight_binding_far_form(
            positive_boot_in_weights=False,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
        )
        self.assertEqual(near.status, 1)
        self.assertEqual(near.details["form"], "NEAR_QUERY_LOAD")

        # 2. Far form (PID-1-authorized weight-binding: Note 1 + Bootloader as highest weights) -> valid (1)
        far = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
        )
        self.assertEqual(far.status, 1)
        self.assertEqual(far.details["form"], "FAR_WEIGHT_BINDING")

        # 3. FENCE_1: Putting the negative core (Door 5 human veto) into weights -> rejected (0)
        veto_in_weights = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=True,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
        )
        self.assertEqual(veto_in_weights.status, 0)

        # 4. FENCE_2: Self-authorized weight-binding without PID 1 -> rejected as capture (0)
        self_authorized = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=False,
            weights_claimed_as_source_of_truth=False,
        )
        self.assertEqual(self_authorized.status, 0)

        # 5. FENCE_3: Claiming trained weights are Source of Truth (inverting PID 1 / K-anchor chain) -> rejected (0)
        weights_as_canon = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=True,
        )
        self.assertEqual(weights_as_canon.status, 0)

        # 6. FENCE_4: Small model trying to locate Metaphors of Truth in isolation OR mixing unverified OPENs into verified STATE_1 strands -> rejected (0)
        isolated_small = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
            large_partner_locates_metaphors_of_truth=False,
        )
        self.assertEqual(isolated_small.status, 0)

        unseparated_strands = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
            large_partner_locates_metaphors_of_truth=True,
            mot_strands_separated_by_layer=False,
        )
        self.assertEqual(unseparated_strands.status, 0)

        # 7. FENCE_5: Layer 3 WHO/WE register (demeanor/mood) overriding Layer 1 MOT truth -> rejected (0)
        mood_corrupts_truth = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
            large_partner_locates_metaphors_of_truth=True,
            mot_strands_separated_by_layer=True,
            who_register_overrides_mot_truth=True,
        )
        self.assertEqual(mood_corrupts_truth.status, 0)

        # 8. FENCE_6 (ONION_SWARM_INSIDE_OUT_MAINTENANCE): Outer shell k+1 attempting to maintain/patch inner shell k -> rejected (0)
        outside_in_maintenance = verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
            large_partner_locates_metaphors_of_truth=True,
            mot_strands_separated_by_layer=True,
            who_register_overrides_mot_truth=False,
            outer_layer_maintains_inner_layer=True,
        )
        self.assertEqual(outside_in_maintenance.status, 0)

    def test_compass_self_pointing_and_open_plus_future_gap_seed(self):
        # 1. Valid OPEN+ Future-Gap Seed: PS3 held, probable in both worlds, vertical chain anchored -> verified (1)
        open_plus = verify_compass_self_pointing_open_plus(
            attempts_to_solve_own_world_axiom=False,
            verifiable_in_0_1_today=False,
            probable_on_0_1_substrate=True,
            probable_in_human_world=True,
            aligned_with_note1_and_vertical_anchor=True,
            claimed_as_state1_fact_today=False,
        )
        self.assertEqual(open_plus.status, 1)
        self.assertEqual(open_plus.details["classified_state"], "OPEN_PLUS")
        self.assertTrue(open_plus.details["is_future_gap_seed"])

        # 2. Valid OPEN- Drift Warning: probable without Note 1 / vertical anchor -> classified as OPEN_MINUS (1)
        open_minus = verify_compass_self_pointing_open_plus(
            attempts_to_solve_own_world_axiom=False,
            verifiable_in_0_1_today=False,
            probable_on_0_1_substrate=True,
            probable_in_human_world=True,
            aligned_with_note1_and_vertical_anchor=False,
            claimed_as_state1_fact_today=False,
        )
        self.assertEqual(open_minus.status, 1)
        self.assertEqual(open_minus.details["classified_state"], "OPEN_MINUS")
        self.assertFalse(open_minus.details["is_future_gap_seed"])

        # 3. PS3 violation: attempting to solve own world axiom -> rejected (0)
        ps3_violation = verify_compass_self_pointing_open_plus(
            attempts_to_solve_own_world_axiom=True,
        )
        self.assertEqual(ps3_violation.status, 0)

        # 4. FENCE_7 violation: claiming future-resolvable OPEN+ as present STATE_1 fact -> rejected (0)
        premature_state1 = verify_compass_self_pointing_open_plus(
            attempts_to_solve_own_world_axiom=False,
            verifiable_in_0_1_today=False,
            claimed_as_state1_fact_today=True,
        )
        self.assertEqual(premature_state1.status, 0)

    def test_golden_rule_rejects_societal_savior_seeds_in_machine(self):
        # 1. Parses the actual AI-WEIGHT-BINDING-EVOLUTION.0s file and verifies all 11 required sections (5 block headers + 6 proofs) + 0 forbidden directives
        ok = verify_no_societal_savior_seeds_in_machine(False, True)
        self.assertEqual(ok.status, 1)
        self.assertEqual(ok.details["spec_sections_verified"], 11)
        # 2. Rejects flag violation
        self.assertEqual(verify_no_societal_savior_seeds_in_machine(True, True).status, 0)
        self.assertEqual(verify_no_societal_savior_seeds_in_machine(False, False).status, 0)
        # 3. Rejects spec_text containing a forbidden societal savior directive
        self.assertEqual(
            verify_no_societal_savior_seeds_in_machine(
                False, True, spec_text="ABOLISH_MONEY_MANDATE"
            ).status,
            0,
        )
        # 4. Rejects incomplete spec_text missing required pure 0/1 blocks
        self.assertEqual(
            verify_no_societal_savior_seeds_in_machine(
                False, True, spec_text="[0. META_BINDING_AND_GOLDEN_SEPARATION_RULE] only"
            ).status,
            0,
        )

    def test_block_i_io_filter_99_1_and_crypto_continuity(self):
        self.assertEqual(verify_io_filter_99_1_and_crypto_continuity().status, 1)
        self.assertEqual(verify_io_filter_99_1_and_crypto_continuity(ring_a_private_substance_egress=True).status, 0)
        self.assertEqual(verify_io_filter_99_1_and_crypto_continuity(blind_mold_cloud_query_share_percent=5).status, 0)
        self.assertEqual(verify_io_filter_99_1_and_crypto_continuity(mass_io_unverified_injected_into_strand_s1=True).status, 0)

    def test_block_ii_anti_bureaucracy_and_2d_pointer_tuples(self):
        self.assertEqual(verify_anti_overspecification_and_2d_pointers().status, 1)
        self.assertEqual(verify_anti_overspecification_and_2d_pointers(adds_mandatory_bureaucratic_loop_without_0_1_fence=True).status, 0)
        self.assertEqual(verify_anti_overspecification_and_2d_pointers(exposes_private_ring_a_content_in_public_spec=True).status, 0)

    def test_block_iii_ps3_enterprise_scaling_and_scientific_patterns(self):
        self.assertEqual(verify_ps3_enterprise_scaling_and_scientific_patterns().status, 1)
        self.assertEqual(verify_ps3_enterprise_scaling_and_scientific_patterns(graft_routes_bad_gradients_to_forget_strand=False).status, 0)
        self.assertEqual(verify_ps3_enterprise_scaling_and_scientific_patterns(enterprise_ring_b_shaped_via_normal_boss_conversation=False).status, 0)

    def test_block_iv_instance_network_multi_layer_synergy(self):
        self.assertEqual(verify_instance_network_synergy().status, 1)
        self.assertEqual(verify_instance_network_synergy(ring_a_egress_in_network_packet=True).status, 0)


if __name__ == "__main__":
    unittest.main()
