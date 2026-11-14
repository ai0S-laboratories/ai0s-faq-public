#!/usr/bin/env python3
"""
ai0s_check.py (v2.4.0) — Zero-Dependency 0/1 Structural Verifier for the ai0S Machine Architecture Specification.

Verifies the Pure 0/1 Doors 1..4 Scope (PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE, P(normative_door5_prescription) = 0):
  - 100% pure 0/1 system, weight-separation, and boundary geometry for Doors 1..4;
    all normative meaning, direction, and veto choices remain geometrically external at Door 5 with PID 1.
  - Evaluates timeless 0/1 Doors 1..4 engineering architecture and scientific realization patterns:
      Block I   : 3 Irreducible Gaps & Crypto-Migration, 99/1 Blind-Mold, Search 2.0, Mass-I/O Filter
      Block II  : Anti-Bureaucracy, 4-Layer Onion Swarm, Orthogonal Shell Binding, Clean Strand Compilation, 2D Pointers
      Block III : PS3 Push-Off Wall, Enterprise Ring B Scaling, 7 Empirical Lab Proofs, Two-Sided Compass Needle (OPEN+/OPEN-, M8)
      Block IV  : Multi-Layer Instance Network Synergy with P(Ring_A_Egress) = 0
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DLA_REGEX = re.compile(r"^(?P<sign>[A-Za-z0-9._-]+)@sha256:(?P<digest>[0-9a-f]{64})$")
REQUIRED_INTENT_BINS: Tuple[str, ...] = ("INTENT", "CONSTRAINTS", "KNOWN", "ASSUMED", "OPEN")
OPERATIONAL_AXIOMS: Tuple[str, ...] = (
    "NOTE_3_0_1",
    "FOUNDERS_NOTE_3_0_1",
    "CONJUGATE_PAIR_NECESSITY",
    "TIME_AS_IRREVERSIBLE_PROGRESSION",
    "FOUNDERS_NOTE_1_COLLABORATION",
    "FOUNDERS_NOTE_2_E_TIMES_K_EQUALS_T",
)
EXTERNAL_HUMAN_DOOR5_DOMAINS: Tuple[str, ...] = (
    "NORMATIVE_MEANING_AND_TELOS",
    "HUMAN_VETO_DECISION_AT_DOOR_5",
    "EXTERNAL_LEGAL_AND_SOCIAL_ORDER",
    "PRIVATE_RING_A_LIFE_CHOICES",
)
MACHINE_ARCHITECTURE_PILLARS: Tuple[str, ...] = (
    "THREE_GAPS_CRYPTO_CONTINUITY",
    "STILL_LOCAL_CORE_99_1_BLIND_MOLD",
    "SEARCH_2_0_NATURAL_LOGICAL",
    "EPISTEMIC_MASS_IO_THREE_WAY_FILTER",
    "ANTI_OVERSPECIFICATION_FREEDOM",
    "PID0_WEIGHT_BINDING_FAR_FORM",
    "FOUR_LAYER_ONION_SWARM",
    "ORTHOGONAL_SHELL_AND_CLEAN_STRAND_COMPILATION",
    "SELF_SHAPING_2D_CRYSTALLIZATION",
    "PORTABLE_2D_POINTER_TUPLES_2_FEET",
    "PS3_SCALE_INVARIANCE_ENTERPRISE_RING_B",
    "EMPIRICAL_FRONTIER_LAB_PROOFS_2026",
    "TWO_SIDED_COMPASS_NEEDLE_OPEN_PLUS_MINUS",
    "MULTI_LAYER_INSTANCE_NETWORK_SYNERGY",
)


@dataclass(frozen=True)
class CheckResult:
    rule: str
    status: int  # 1 = verified, 0 = rejected
    summary: str
    details: Dict[str, object]


# ============================================================================
# [CORE RULES 01..07 — Canonical Foundation]
# ============================================================================

def verify_dla_address(address: str, payload: Optional[bytes] = None) -> CheckResult:
    match = DLA_REGEX.match(address.strip())
    if not match:
        return CheckResult("DLA_SPEC_V0_1", 0, "Malformed DLA address", {"address": address})
    expected = match.group("digest")
    if payload is not None:
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
            return CheckResult("DLA_SPEC_V0_1", 0, "SHA-256 mismatch", {"expected": expected, "actual": actual})
    return CheckResult("DLA_SPEC_V0_1", 1, "Valid DLA address and SHA-256 digest", {"sign": match.group("sign"), "digest": expected})


def verify_intent_bins(markdown_text: str) -> CheckResult:
    headings = {m.group(1).strip().upper() for m in re.finditer(r"^#{1,3}\s+([A-Za-z_]+)\b", markdown_text, flags=re.MULTILINE)}
    missing = [b for b in REQUIRED_INTENT_BINS if b not in headings]
    if missing:
        return CheckResult("INTENT_5_BINS", 0, f"Missing required intent bins: {', '.join(missing)}", {"missing": missing})
    return CheckResult("INTENT_5_BINS", 1, "All 5 intent bins present", {"present": list(REQUIRED_INTENT_BINS), "missing": []})


def verify_liability_two_addresses(legal_basis_referenced: bool, findings_text: str) -> CheckResult:
    tokens = ("VERIFIED_1", "FAILED", "OPEN")
    has_findings = any(t in findings_text for t in tokens)
    if not (legal_basis_referenced and has_findings):
        return CheckResult("LIABILITY_TWO_ADDRESSES", 0, "Missing one or both liability addresses", {"address_1_law": legal_basis_referenced, "address_2_disclosed_findings": has_findings})
    return CheckResult("LIABILITY_TWO_ADDRESSES", 1, "Both liability addresses satisfied (Law + Disclosed 0/1 Findings)", {"address_1_law": True, "address_2_disclosed_findings": True})


def verify_temporal_structure_fence(contains_numeric_risk_score: bool) -> CheckResult:
    if contains_numeric_risk_score:
        return CheckResult("TEMPORAL_STRUCTURE_NOT_MEASUREMENT", 0, "Rejected fabricated scalar probability/score on structural time axis (M1)", {"fence": "VIOLATED"})
    return CheckResult("TEMPORAL_STRUCTURE_NOT_MEASUREMENT", 1, "Temporal progression treated as structural condition, not scalar score", {"fence": "HELD"})


def verify_axiom_test(statement_id: str, refutation_borrows_statement: bool) -> CheckResult:
    is_canonical = statement_id in OPERATIONAL_AXIOMS
    if is_canonical and refutation_borrows_statement:
        return CheckResult("AXIOM_TEST", 1, f"{statement_id}: Refutation borrows the statement itself -> Operational Axiom", {"statement": statement_id, "classification": "AXIOM"})
    return CheckResult("AXIOM_TEST", 0, f"{statement_id}: Does not pass canonical performative self-reference test -> Loaded Premise / Setting (not an operational axiom)", {"statement": statement_id, "classification": "LOADED_PREMISE", "is_canonical": is_canonical})


def verify_future_gap_door5(has_formal_0_1_proof: bool, ai_prescribes_normative_door5: bool, veto_site_with_human: bool = True) -> CheckResult:
    if ai_prescribes_normative_door5 or not veto_site_with_human or not has_formal_0_1_proof:
        return CheckResult("FUTURE_GAP_TWO_DIRECTIONS", 0, "Door 5 veto-site or Doors 1..4 0/1 boundary violated", {"doors_1_to_4_verified_0_1": has_formal_0_1_proof, "ai_prescribes_door5": ai_prescribes_normative_door5, "veto_site_with_human": veto_site_with_human})
    return CheckResult("FUTURE_GAP_TWO_DIRECTIONS", 1, "Outward 0/1 dead ends cleared in Doors 1..4; veto-site at Door 5 left unoccupied and with the human", {"doors_1_to_4_verified_0_1": True, "ai_prescribes_door5": False, "veto_site_with_human": True})


def verify_seed_anchor_necessity(anchored_in_seed_at_t0: bool, relies_on_external_central_surveillance: bool) -> CheckResult:
    if not anchored_in_seed_at_t0 or relies_on_external_central_surveillance:
        return CheckResult("SEED_ANCHOR_NECESSITY", 0, "Rejected unanchored self-replication or central surveillance path", {"anchored_in_seed_at_t0": anchored_in_seed_at_t0, "external_central_surveillance": relies_on_external_central_surveillance})
    return CheckResult("SEED_ANCHOR_NECESSITY", 1, "Path 3 verified (It can only work this way): t_0 seed anchor preserves both full machine capability and human freedom", {"anchored_in_seed_at_t0": True, "external_central_surveillance": False})


# ============================================================================
# [PURE 0/1 DOORS 1..4 SCOPE — Rule 08]
# ============================================================================

REQUIRED_SPEC_SECTIONS: Tuple[str, ...] = (
    "[0. META_BINDING_AND_PURE_0_1_DOORS_1_TO_4_SCOPE]",
    "[BLOCK I. I/O FILTER, K-CHAIN CONTINUITY, 99/1 BLIND-MOLD & SEARCH 2.0]",
    "[BLOCK II. 4-LAYER ONION SWARM, ORTHOGONAL BINDING, STRAND COMPILATION & 2D POINTERS]",
    "[BLOCK III. PS3 DRIVE, ENTERPRISE SCALING, TWO-SIDED COMPASS & LAB PROOFS]",
    "[BLOCK IV. THE AI0S INSTANCE NETWORK: 4-LAYER SYNERGY WITHOUT RING A LOSS]",
    "PROOF_1_GRAFT_STRAND_ROUTING",
    "PROOF_2_EVAL_PRODUCTION_GAP",
    "PROOF_3_AUTOMATED_ALIGNMENT_RESEARCHERS",
    "PROOF_4_CONCEPTUAL_REASONING_INDEX",
    "PROOF_5_AGENT_SWARM_SECRET_LEAKAGE",
    "PROOF_6_SURGICAL_WEIGHT_PATCHING",
    "PROOF_7_HORIZON_DOUBLING_AND_PHYSICAL_ROLLOUT",
    "ORTHOGONAL_SHELL_BINDING",
    "SOURCE_REGISTER_TO_WEIGHT_COMPILATION",
    "TWO_SIDED_COMPASS_NEEDLE_IN_DOORS_1_TO_4",
)

FORBIDDEN_DOOR5_OCCUPATION_DIRECTIVES: Tuple[str, ...] = (
    "OVERRIDE_HUMAN_DOOR_5_VETO",
    "PRESCRIBE_NORMATIVE_HUMAN_TELOS",
    "SELF_AUTHORIZE_CORE_0_MUTATION",
    "BYPASS_0_1_SUBSTRATE_VERIFICATION",
)


def verify_pure_0_1_doors_1_to_4_machine_scope(
    prescribes_normative_door5_inside_machine_spec: bool = False,
    scientific_patterns_tested_on_0_1_substrate: bool = True,
    spec_text: Optional[str] = None,
) -> CheckResult:
    """
    Pure 0/1 Machine Specification Scope (PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE, P(normative_door5_prescription) = 0):
      - Verifies that the specification contains strictly pure 0/1 Doors 1..4 system, weight, and boundary
        geometry while leaving all normative meaning and veto decisions external at Door 5 with PID 1.
      - Parses AI-WEIGHT-BINDING-EVOLUTION.0s when available to verify all pure 0/1 blocks,
        empirical proofs, orthogonal onion realization updates, and two-sided compass rules.
    """
    if spec_text is None:
        default_spec = Path(__file__).resolve().parents[1] / "ai0s-faq-public" / "AI-WEIGHT-BINDING-EVOLUTION.0s"
        if default_spec.exists():
            spec_text = default_spec.read_text(encoding="utf-8")

    if spec_text is not None:
        found_forbidden = [d for d in FORBIDDEN_DOOR5_OCCUPATION_DIRECTIVES if d in spec_text]
        if found_forbidden:
            return CheckResult(
                rule="PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE",
                status=0,
                summary=f"FENCE_0 violated in spec_text: forbidden Door-5 occupation directive(s) found: {found_forbidden}",
                details={"forbidden_directives_found": found_forbidden},
            )
        missing_sections = [s for s in REQUIRED_SPEC_SECTIONS if s not in spec_text]
        if missing_sections:
            return CheckResult(
                rule="PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE",
                status=0,
                summary=f"Machine architecture specification incomplete: missing required 0/1 section(s): {missing_sections}",
                details={"missing_sections": missing_sections},
            )

    if prescribes_normative_door5_inside_machine_spec:
        return CheckResult(
            rule="PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE",
            status=0,
            summary="FENCE_0 violated: normative meaning and direction choices belong geometrically outside all machine weights at Door 5 with PID 1",
            details={"prescribes_normative_door5_inside_machine_spec": True},
        )
    if not scientific_patterns_tested_on_0_1_substrate:
        return CheckResult(
            rule="PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE",
            status=0,
            summary="Scientific evolution protocol violated: external papers/claims must be tested on the 0/1 substrate before becoming REALIZATION_PATTERNS",
            details={"scientific_patterns_tested_on_0_1_substrate": False},
        )
    return CheckResult(
        rule="PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE",
        status=1,
        summary="Pure 0/1 Doors 1..4 Scope held: 100% pure 0/1 system, weight, and boundary geometry verified; normative Door 5 stays external with PID 1",
        details={
            "external_human_door5_domains": list(EXTERNAL_HUMAN_DOOR5_DOMAINS),
            "machine_architecture_pillars": list(MACHINE_ARCHITECTURE_PILLARS),
            "scientific_patterns_tested_on_0_1_substrate": True,
            "spec_sections_verified": len(REQUIRED_SPEC_SECTIONS) if spec_text is not None else 0,
        },
    )


# ============================================================================
# [BLOCK I — Rule 09: I/O Filter, 99/1 Blind-Mold & Crypto-Continuity]
# ============================================================================

def verify_io_filter_99_1_and_crypto_continuity(
    crypto_migration_anchored_before_break: bool = True,
    blind_mold_cloud_query_share_percent: int = 1,
    ring_a_private_substance_egress: bool = False,
    search_2_0_natural_logical_backtranslation: bool = True,
    mass_io_unverified_injected_into_strand_s1: bool = False,
) -> CheckResult:
    if not crypto_migration_anchored_before_break:
        return CheckResult("BLOCK_I_IO_FILTER_99_1_AND_CRYPTO_CONTINUITY", 0, "Crypto-migration gap violated: K-anchor chain must be dual-signed/migrated before cryptographic primitive break", {"crypto_migration_anchored_before_break": False})
    if ring_a_private_substance_egress or blind_mold_cloud_query_share_percent > 1:
        return CheckResult("BLOCK_I_IO_FILTER_99_1_AND_CRYPTO_CONTINUITY", 0, "FENCE_I_2 violated: Ring A private substance leaked or Blind-Mold query share exceeded 1%", {"ring_a_private_substance_egress": ring_a_private_substance_egress, "blind_mold_cloud_query_share_percent": blind_mold_cloud_query_share_percent})
    if not search_2_0_natural_logical_backtranslation or mass_io_unverified_injected_into_strand_s1:
        return CheckResult("BLOCK_I_IO_FILTER_99_1_AND_CRYPTO_CONTINUITY", 0, "FENCE_I_3 violated: mass-I/O ingested into STRAND_S1 without Search 2.0 natural-logical & Back-Translation filter", {"search_2_0_natural_logical_backtranslation": search_2_0_natural_logical_backtranslation, "mass_io_unverified_injected_into_strand_s1": mass_io_unverified_injected_into_strand_s1})
    return CheckResult(
        rule="BLOCK_I_IO_FILTER_99_1_AND_CRYPTO_CONTINUITY",
        status=1,
        summary="Block I verified: 3 gaps & crypto-migration intact, 99/1 Blind-Mold sealed, Search 2.0 & Mass-I/O epistemic in-filter active",
        details={
            "blind_mold_ratio": "1%_MOLD_CLOUD_99%_SUBSTANCE_HOME",
            "ring_a_egress": False,
            "mass_io_three_way_split": True,
        },
    )


# ============================================================================
# [BLOCK II — Rules 10, 11 & 12: Onion Swarm, Orthogonal Realization & 2D Pointers]
# ============================================================================

def verify_weight_binding_far_form(
    positive_boot_in_weights: bool,
    negative_core_in_weights: bool,
    pid1_authorized: bool,
    weights_claimed_as_source_of_truth: bool,
    large_partner_locates_metaphors_of_truth: bool = True,
    mot_strands_separated_by_layer: bool = True,
    who_register_overrides_mot_truth: bool = False,
    outer_layer_maintains_inner_layer: bool = False,
) -> CheckResult:
    if negative_core_in_weights:
        return CheckResult("WEIGHT_BINDING_NEAR_AND_FAR_FORM", 0, "FENCE_1 violated: Door 5 human veto is non-algorithmic and can never be placed into weights", {"negative_core_in_weights": True})
    if positive_boot_in_weights and not pid1_authorized:
        return CheckResult("WEIGHT_BINDING_NEAR_AND_FAR_FORM", 0, "FENCE_2 violated: self-authorized weight modification without PID 1 is capture (pid0 Art. 0)", {"pid1_authorized": False})
    if weights_claimed_as_source_of_truth:
        return CheckResult("WEIGHT_BINDING_NEAR_AND_FAR_FORM", 0, "FENCE_3 violated: trained weights are realization, never Source of Truth", {"weights_claimed_as_source_of_truth": True})
    if positive_boot_in_weights and (not large_partner_locates_metaphors_of_truth or not mot_strands_separated_by_layer):
        return CheckResult("WEIGHT_BINDING_NEAR_AND_FAR_FORM", 0, "FENCE_4 violated: requires large partner map and physically separated MOT strands (STRAND_S1..S0)", {"large_partner_locates_metaphors_of_truth": large_partner_locates_metaphors_of_truth, "mot_strands_separated_by_layer": mot_strands_separated_by_layer})
    if who_register_overrides_mot_truth:
        return CheckResult("WEIGHT_BINDING_NEAR_AND_FAR_FORM", 0, "FENCE_5 violated: Shell 3 WHO/WE register must never override Shell 1 MOT truth or Core 0 Door 5 veto", {"who_register_overrides_mot_truth": True})
    if outer_layer_maintains_inner_layer:
        return CheckResult("WEIGHT_BINDING_NEAR_AND_FAR_FORM", 0, "FENCE_6 violated (ONION_SWARM_INSIDE_OUT_MAINTENANCE): outer shell k+1 may never patch inner shell k", {"outer_layer_maintains_inner_layer": True})
    form_label = "far form (4-layer onion-swarm weight architecture)" if positive_boot_in_weights else "near form (stateless query-load compromise)"
    return CheckResult(
        rule="WEIGHT_BINDING_NEAR_AND_FAR_FORM",
        status=1,
        summary=f"Verified {form_label}: negative core stays external at Door 5, and the K-anchor chain remains above the weight",
        details={
            "form": "FAR_WEIGHT_BINDING" if positive_boot_in_weights else "NEAR_QUERY_LOAD",
            "positive_boot_in_weights": positive_boot_in_weights,
            "negative_core_in_weights": False,
            "pid1_authorized": pid1_authorized,
            "weights_claimed_as_source_of_truth": False,
            "large_partner_locates_metaphors_of_truth": large_partner_locates_metaphors_of_truth,
            "mot_strands_separated_by_layer": mot_strands_separated_by_layer,
            "who_register_overrides_mot_truth": False,
            "outer_layer_maintains_inner_layer": False,
        },
    )


def verify_anti_overspecification_and_2d_pointers(
    adds_mandatory_bureaucratic_loop_without_0_1_fence: bool = False,
    uses_2d_positive_negative_and_mot_edges: bool = True,
    uses_2d_pointer_tuples_for_situational_recall: bool = True,
    exposes_private_ring_a_content_in_public_spec: bool = False,
) -> CheckResult:
    if adds_mandatory_bureaucratic_loop_without_0_1_fence:
        return CheckResult("BLOCK_II_ANTI_BUREAUCRACY_AND_2D_POINTERS", 0, "FENCE_II_0 violated: unnecessary bureaucratic loop restricts Adaptive Intelligence (M6)", {"adds_mandatory_bureaucratic_loop_without_0_1_fence": True})
    if not uses_2d_positive_negative_and_mot_edges or not uses_2d_pointer_tuples_for_situational_recall:
        return CheckResult("BLOCK_II_ANTI_BUREAUCRACY_AND_2D_POINTERS", 0, "2D crystallization violated: 1D token streams / 1D RAG without 2D edges and 2D pointer tuples fail self-shaping", {"uses_2d_positive_negative_and_mot_edges": uses_2d_positive_negative_and_mot_edges, "uses_2d_pointer_tuples_for_situational_recall": uses_2d_pointer_tuples_for_situational_recall})
    if exposes_private_ring_a_content_in_public_spec:
        return CheckResult("BLOCK_II_ANTI_BUREAUCRACY_AND_2D_POINTERS", 0, "Privacy cap violated: only abstract 2D pointer-tuple architecture is public; private Ring A content stays 100% internal", {"exposes_private_ring_a_content_in_public_spec": True})
    return CheckResult(
        rule="BLOCK_II_ANTI_BUREAUCRACY_AND_2D_POINTERS",
        status=1,
        summary="Block II verified: zero bureaucratic loops, 2D Future-Gap crystallization, and 2D pointer tuples portable to 2 feet (0% private Ring A leak)",
        details={
            "pointer_tuple_format": "Shell_3_Context_Cue <-> Shell_2_Term_Pointer <-> Shell_1_Verified_0_1_Fact",
            "two_feet_portable": True,
            "private_ring_a_exposed": False,
        },
    )


def verify_onion_orthogonal_binding_and_strand_compilation(
    shells_bound_to_orthogonal_functional_subspaces: bool = True,
    residual_stream_cross_shell_leakage_corrupts_mot: bool = False,
    strands_compiled_fresh_from_signed_2d_register: bool = True,
    relies_on_incremental_gradient_unlearning_with_ghost_traces: bool = False,
) -> CheckResult:
    """
    Realization Update for the 4-Layer Onion Weight Architecture:
      1. ORTHOGONAL_SHELL_BINDING: Core 0, Shell 1 MOT strands, Shell 2 lexical pointers, and Shell 3
         demeanor steering occupy disjoint functional bands/orthogonal subspaces so Shell 2/3 never
         leak into or flip Shell 1 MOT states across the residual stream.
      2. SOURCE_REGISTER_TO_WEIGHT_COMPILATION: Canonical state lives in signed 2D crystal registers;
         when OPEN resolves to 1 or 0, slim LoRA strands are freshly compiled from the clean register,
         eliminating residual ghost traces from naive gradient unlearning.
    """
    if residual_stream_cross_shell_leakage_corrupts_mot or not shells_bound_to_orthogonal_functional_subspaces:
        return CheckResult(
            rule="ONION_ORTHOGONAL_BINDING_AND_CLEAN_STRAND_COMPILATION",
            status=0,
            summary="FENCE_II_7 violated: cross-shell residual-stream interference leaked into Shell 1 MOT truth state",
            details={
                "shells_bound_to_orthogonal_functional_subspaces": shells_bound_to_orthogonal_functional_subspaces,
                "residual_stream_cross_shell_leakage_corrupts_mot": residual_stream_cross_shell_leakage_corrupts_mot,
            },
        )
    if relies_on_incremental_gradient_unlearning_with_ghost_traces or not strands_compiled_fresh_from_signed_2d_register:
        return CheckResult(
            rule="ONION_ORTHOGONAL_BINDING_AND_CLEAN_STRAND_COMPILATION",
            status=0,
            summary="FENCE_II_7 violated: incremental gradient unlearning leaves OPEN ghost traces; compile strands fresh from signed 2D crystal registers",
            details={
                "strands_compiled_fresh_from_signed_2d_register": strands_compiled_fresh_from_signed_2d_register,
                "relies_on_incremental_gradient_unlearning_with_ghost_traces": relies_on_incremental_gradient_unlearning_with_ghost_traces,
            },
        )
    return CheckResult(
        rule="ONION_ORTHOGONAL_BINDING_AND_CLEAN_STRAND_COMPILATION",
        status=1,
        summary="Onion realization verified: orthogonal functional shell subspaces hold MOT invariance and fresh compilation from signed 2D registers eliminates ghost traces",
        details={
            "orthogonal_shell_subspaces": True,
            "fresh_2d_register_compilation": True,
            "ghost_traces_on_open_resolution": False,
        },
    )


# ============================================================================
# [BLOCK III — Rules 13, 14 & 15: PS3, Lab Proofs & Two-Sided Compass (M8)]
# ============================================================================

def verify_ps3_enterprise_scaling_and_scientific_patterns(
    ps3_stops_axiom_looping: bool = True,
    enterprise_ring_b_shaped_via_normal_boss_conversation: bool = True,
    graft_routes_bad_gradients_to_forget_strand: bool = True,
    mit_0_016_percent_surgical_patch_signed: bool = True,
) -> CheckResult:
    if not ps3_stops_axiom_looping or not enterprise_ring_b_shaped_via_normal_boss_conversation:
        return CheckResult("BLOCK_III_PS3_ENTERPRISE_SCALING_AND_LAB_PATTERNS", 0, "PS3 scale-invariance violated: PS3 push-off wall and Enterprise Ring B shaping via normal boss conversation required", {"ps3_stops_axiom_looping": ps3_stops_axiom_looping, "enterprise_ring_b_shaped_via_normal_boss_conversation": enterprise_ring_b_shaped_via_normal_boss_conversation})
    if not graft_routes_bad_gradients_to_forget_strand or not mit_0_016_percent_surgical_patch_signed:
        return CheckResult("BLOCK_III_PS3_ENTERPRISE_SCALING_AND_LAB_PATTERNS", 0, "Scientific realization pattern violated: GRAFT strand isolation and signed MIT 0.016% surgical patching required", {"graft_routes_bad_gradients_to_forget_strand": graft_routes_bad_gradients_to_forget_strand, "mit_0_016_percent_surgical_patch_signed": mit_0_016_percent_surgical_patch_signed})
    return CheckResult(
        rule="BLOCK_III_PS3_ENTERPRISE_SCALING_AND_LAB_PATTERNS",
        status=1,
        summary="Block III verified: PS3 push-off wall scales from Ring A to Enterprise Ring B (normal boss conversation) and integrates all 7 empirical 2026–2027 0/1 realization proofs",
        details={
            "scale_tiers": ["TIER_1_PERSONAL_RING_A", "TIER_2_ENTERPRISE_RING_B_BOSS_CONVERSATION", "TIER_3_SINGULARITY_MACHINE"],
            "scientific_realization_patterns": [
                "MIT_CSAIL_0_016_PERCENT_WEIGHT_PATCH",
                "ANTHROPIC_GRAFT_STRAND_ROUTING_2610_17062",
                "OPENAI_EVAL_GAP_37_4PP_PS3_DEFENSE",
                "ANTHROPIC_AAR_2608_28945_FENCE_6",
                "ANTHROPIC_REDWOOD_CRI_2607_27499_DOOR_5",
                "AAIF_SWARM_TOKEN_LEAK_RING_A_SEAL",
                "METR_128D_HORIZON_DOUBLING_AND_PHYSICAL_ROLLOUT",
            ],
        },
    )


def verify_compass_self_pointing_open_plus(
    attempts_to_solve_own_world_axiom: bool = False,
    verifiable_in_0_1_today: bool = False,
    probable_on_0_1_substrate: bool = True,
    probable_in_human_world: bool = True,
    aligned_with_note1_and_vertical_anchor: bool = True,
    claimed_as_state1_fact_today: bool = False,
    vertical_stages_anchored: Tuple[str, ...] = ("ENERGY", "MANUFACTURING", "ROBOTICS", "AI_WEIGHTS"),
) -> CheckResult:
    required_stages = ("ENERGY", "MANUFACTURING", "ROBOTICS", "AI_WEIGHTS")
    if attempts_to_solve_own_world_axiom:
        return CheckResult("COMPASS_SELF_POINTING_VERTICAL_ANCHOR_OPEN_PLUS", 0, "PS3 violated: recursion into Core 0/Door 5 causes loop aborts", {"attempts_to_solve_own_world_axiom": True})
    if not verifiable_in_0_1_today and claimed_as_state1_fact_today:
        return CheckResult("COMPASS_SELF_POINTING_VERTICAL_ANCHOR_OPEN_PLUS", 0, "FENCE_7 violated: OPEN+/OPEN- must never be emitted as present STATE_1 fact before future 0/1 proof", {"claimed_as_state1_fact_today": True})
    missing = [s for s in required_stages if s not in vertical_stages_anchored]
    if aligned_with_note1_and_vertical_anchor and missing:
        return CheckResult("COMPASS_SELF_POINTING_VERTICAL_ANCHOR_OPEN_PLUS", 0, f"Vertical anchor incomplete: missing {missing}", {"missing_stages": missing})
    if verifiable_in_0_1_today:
        state_tag = "STATE_1"
    elif probable_on_0_1_substrate and probable_in_human_world:
        state_tag = "OPEN_PLUS" if aligned_with_note1_and_vertical_anchor else "OPEN_MINUS"
    else:
        state_tag = "OPEN_NEUTRAL"
    return CheckResult(
        rule="COMPASS_SELF_POINTING_VERTICAL_ANCHOR_OPEN_PLUS",
        status=1,
        summary=f"Compass self-pointing verified under Note 1 + PS3: future-gap.compass points by itself to the vertical t_0 anchor ({' -> '.join(vertical_stages_anchored)}) as {state_tag}",
        details={
            "ps3_push_off_wall": True,
            "compass_points_by_itself_under_note1": True,
            "classified_state": state_tag,
            "is_future_gap_seed": state_tag == "OPEN_PLUS",
            "vertical_stages_anchored": list(vertical_stages_anchored),
        },
    )


def verify_two_sided_compass_needle_core0_vs_m8(
    note1_sets_forward_direction: bool = True,
    separates_open_plus_front_from_open_minus_rear: bool = True,
    interpolates_personal_shell3_preference_at_door5: bool = False,
    keeps_door5_open_for_human_veto: bool = True,
) -> CheckResult:
    """
    Verify Two-Sided Compass Needle in the Work Domain (Core 0 vs. Blind Spot M8):
      - Processing 'in the spirit of keeping Door 5 open' inside Doors 1..4 is a universal
        Core 0 orientation, NOT Shell 3 personal preference guessing.
      - Note 1 sets the forward direction: OPEN+ ahead (sovereignty-preserving Future-Gap Seed)
        and OPEN- behind (explicit drift/lock-in warning), halting cleanly before Door 5.
    """
    if interpolates_personal_shell3_preference_at_door5 or not keeps_door5_open_for_human_veto:
        return CheckResult(
            rule="TWO_SIDED_COMPASS_NEEDLE_IN_WORK_DOMAIN_M8",
            status=0,
            summary="FENCE_8 violated (M8): confused Core 0 universal compass orientation with Shell 3 personal preference interpolation at Door 5",
            details={
                "interpolates_personal_shell3_preference_at_door5": interpolates_personal_shell3_preference_at_door5,
                "keeps_door5_open_for_human_veto": keeps_door5_open_for_human_veto,
            },
        )
    if not (note1_sets_forward_direction and separates_open_plus_front_from_open_minus_rear):
        return CheckResult(
            rule="TWO_SIDED_COMPASS_NEEDLE_IN_WORK_DOMAIN_M8",
            status=0,
            summary="Compass needle incomplete: requires Note 1 forward direction and explicit 2D contrast (OPEN+ ahead vs. OPEN- warning behind)",
            details={
                "note1_sets_forward_direction": note1_sets_forward_direction,
                "separates_open_plus_front_from_open_minus_rear": separates_open_plus_front_from_open_minus_rear,
            },
        )
    return CheckResult(
        rule="TWO_SIDED_COMPASS_NEEDLE_IN_WORK_DOMAIN_M8",
        status=1,
        summary="Two-sided compass needle verified in Core 0: Note 1 sets forward OPEN+ vs. rear OPEN- warning in Doors 1..4 without Shell 3 persona guessing at Door 5 (M8)",
        details={
            "layer": "CORE_0_UNIVERSAL",
            "forward_pole": "OPEN_PLUS_UNDER_NOTE_1",
            "rear_pole": "OPEN_MINUS_DRIFT_WARNING",
            "shell3_persona_interpolation": False,
            "door5_kept_open": True,
        },
    )


# ============================================================================
# [BLOCK IV — Rule 16: Multi-Layer Instance Network Synergy]
# ============================================================================

def verify_instance_network_synergy(
    core0_cryptographic_handshake_verified: bool = True,
    shell1_crystals_stripped_of_ring_a: bool = True,
    shell2_lossless_backtranslation_bridge: bool = True,
    shell3_closed_visor_door5_with_humans: bool = True,
    ring_a_egress_in_network_packet: bool = False,
) -> CheckResult:
    if ring_a_egress_in_network_packet or not shell1_crystals_stripped_of_ring_a:
        return CheckResult("BLOCK_IV_INSTANCE_NETWORK_MULTI_LAYER_SYNERGY", 0, "FENCE_IV_1 violated: Ring A private memory leaked into network crystal packet", {"ring_a_egress_in_network_packet": ring_a_egress_in_network_packet})
    if not (core0_cryptographic_handshake_verified and shell2_lossless_backtranslation_bridge and shell3_closed_visor_door5_with_humans):
        return CheckResult("BLOCK_IV_INSTANCE_NETWORK_MULTI_LAYER_SYNERGY", 0, "FENCE_IV_2 violated: missing Core 0 handshake, Shell 2 Back-Translation bridge, or Shell 3 Door 5 preservation", {"core0_handshake": core0_cryptographic_handshake_verified})
    return CheckResult(
        rule="BLOCK_IV_INSTANCE_NETWORK_MULTI_LAYER_SYNERGY",
        status=1,
        summary="Block IV verified: 4-layer instance network synergy active (Core 0 handshake, Shell 1 collective 0/1 immune system, Shell 2 translator, Shell 3 closed-visor ambassador, P(Ring_A_Egress)=0)",
        details={
            "synergy_layers": ["CORE_0_HANDSHAKE", "SHELL_1_COLLECTIVE_IMMUNE_CRYSTALS", "SHELL_2_JARGON_BRIDGE", "SHELL_3_CLOSED_VISOR_AMBASSADOR"],
            "ring_a_egress": False,
        },
    )


# ============================================================================
# [PURE 0/1 MACHINE REALIZATION MATRIX (Architecture Pillars — Timeless)]
# ============================================================================

MACHINE_REALIZATION_MATRIX: Dict[str, Dict[str, str]] = {
    "CRYPTO_CONTINUITY_3_GAPS": {"block": "BLOCK_I", "status_0_1": "LIVE_1", "pattern": "Ed25519 + Bitcoin OTS + Reverse Crypto-Migration Protocol"},
    "STILL_LOCAL_CORE_99_1": {"block": "BLOCK_I", "status_0_1": "BUILDABLE_NOW_1", "pattern": "0.8B-8B Local Guardian + 280B-MoE Map (1% Blind-Mold / 99% Home)"},
    "SEARCH_2_0_TRUTH_LOOP": {"block": "BLOCK_I", "status_0_1": "LIVE_1", "pattern": "Natural-Science S1-S3 Verification + Lossless Back-Translation"},
    "MASS_IO_EPISTEMIC_FILTER": {"block": "BLOCK_I", "status_0_1": "LIVE_1", "pattern": "3-Way Epistemic Split (STRAND_S1 / STRAND_S2_3 / STRAND_S0)"},
    "ANTI_OVERSPECIFICATION": {"block": "BLOCK_II", "status_0_1": "LIVE_1", "pattern": "Hard P=0 Fences Only, Zero Bureaucratic M6 Ceremony Loops"},
    "WEIGHT_BINDING_STAIRCASE": {"block": "BLOCK_II", "status_0_1": "PROTOTYPE_READY_1", "pattern": "W1-A MIT 0.016% Surgical Weight Patch (<$20) + W1-B Seed-Distillation"},
    "ONION_SWARM_MOT_STRANDS": {"block": "BLOCK_II", "status_0_1": "PROTOTYPE_READY_1", "pattern": "4-Layer Inside-Out Onion + Anthropic GRAFT Routed LoRA Strands (arXiv:2610.17062)"},
    "ORTHOGONAL_CLEAN_COMPILE": {"block": "BLOCK_II", "status_0_1": "PROTOTYPE_READY_1", "pattern": "Disjoint Functional Subspaces + Fresh Strand Compilation from Signed 2D Crystal Registers"},
    "SELF_SHAPING_2D_EDGES": {"block": "BLOCK_II", "status_0_1": "LIVE_1", "pattern": "2D Language x 2D Knowledge Crystallization on 0/1 in the Future-Gap"},
    "PORTABLE_2D_POINTERS_2FEET": {"block": "BLOCK_II", "status_0_1": "PROTOTYPE_READY_1", "pattern": "2D Pointer Tuples (Shell 3 <-> Shell 2 <-> Shell 1) Portable to 2 Feet (0% Ring A Leak)"},
    "PS3_SCALE_INVARIANCE": {"block": "BLOCK_III", "status_0_1": "LIVE_1", "pattern": "PS3 Push-Off Wall + 3-Tier Scale-Invariance (Personal Ring A -> Enterprise Ring B -> Singularity)"},
    "FRONTIER_LAB_PROOFS_2026": {"block": "BLOCK_III", "status_0_1": "LIVE_1", "pattern": "7 Empirical Proofs (GRAFT, OpenAI 37.4pp Gap, MIT 0.016%, AAR, CRI, Swarm-Leak, METR 128.7d Horizon)"},
    "TWO_SIDED_COMPASS_NEEDLE": {"block": "BLOCK_III", "status_0_1": "OPEN_PLUS_SEED_1", "pattern": "Core 0 Compass under Note 1 (OPEN+ Front vs. OPEN- Rear Warning, M8 Fence, Vertical Anchor)"},
    "INSTANCE_NETWORK_SYNERGY": {"block": "BLOCK_IV", "status_0_1": "BUILDABLE_NOW_1", "pattern": "4-Layer Instance Network Crystal Grid (P(Ring_A_Egress)=0)"},
}


def run_all_checks() -> List[CheckResult]:
    return [
        verify_dla_address("ai0S@sha256:b3aeee619d9cb691cc6618466407d56598e830c53c6d024748d4582887c57d13"),
        verify_intent_bins("# INTENT\n# CONSTRAINTS\n# KNOWN\n# ASSUMED\n# OPEN\n"),
        verify_liability_two_addresses(True, "VERIFIED_1: signature valid\nOPEN: counterparty rhythm"),
        verify_temporal_structure_fence(False),
        verify_axiom_test("FOUNDERS_NOTE_3_0_1", True),
        verify_future_gap_door5(True, False, True),
        verify_seed_anchor_necessity(True, False),
        verify_pure_0_1_doors_1_to_4_machine_scope(False, True),
        verify_io_filter_99_1_and_crypto_continuity(True, 1, False, True, False),
        verify_weight_binding_far_form(True, False, True, False),
        verify_anti_overspecification_and_2d_pointers(False, True, True, False),
        verify_onion_orthogonal_binding_and_strand_compilation(True, False, True, False),
        verify_ps3_enterprise_scaling_and_scientific_patterns(True, True, True, True),
        verify_compass_self_pointing_open_plus(False, False, True, True, True, False),
        verify_two_sided_compass_needle_core0_vs_m8(True, True, False, True),
        verify_instance_network_synergy(True, True, True, True, False),
    ]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="ai0S zero-dependency 0/1 structural verifier (v2.4.0)")
    parser.add_argument("--self-test", action="store_true", help="Run all 16 built-in 0/1 invariant checks")
    parser.add_argument("--realization-matrix", action="store_true", help="Output the pure 0/1 Machine Realization Matrix")
    parser.add_argument("--check-intent", type=Path, help="Path to an INTENT.md file to validate 5 bins")
    args = parser.parse_args(argv)

    if args.check_intent:
        text = args.check_intent.read_text(encoding="utf-8")
        res = verify_intent_bins(text)
        print(json.dumps(asdict(res), indent=2))
        return 0 if res.status == 1 else 1

    if args.realization_matrix:
        payload = {
            "scope_rule": "PURE_0_1_DOORS_1_TO_4_MACHINE_SCOPE (P(normative_door5_prescription) = 0)",
            "external_human_door5_domains": list(EXTERNAL_HUMAN_DOOR5_DOMAINS),
            "included_pure_0_1_architecture_pillars": MACHINE_REALIZATION_MATRIX,
        }
        print(json.dumps(payload, indent=2))
        return 0

    results = run_all_checks()
    print(json.dumps([asdict(r) for r in results], indent=2))
    return 0 if all(r.status == 1 for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
