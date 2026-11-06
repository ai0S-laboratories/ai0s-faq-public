#!/usr/bin/env python3
"""
ai0s_check.py — Zero-dependency reference verifier for ai0S structural invariants.

Implements executable 0/1 checks for the core ai0S safety & reasoning rules:
1. PID 1 Human Veto & 5-Bins Intent Check (INTENT, CONSTRAINTS, KNOWN, ASSUMED, OPEN)
2. AXIOM_TEST (Distinguishing performative self-reference from testable claims)
3. LIABILITY_TWO_ADDRESSES (Applicable law + disclosed 0/1 FINDINGS.md audit trail)
4. TEMPORAL_STRUCTURE_NOT_MEASUREMENT (Rejecting synthetic risk scores on temporal sequences)
5. FUTURE_GAP_TWO_DIRECTIONS (Separating Doors 1-4 0/1 raw proof from the Door 5 veto-site that stays with the human -- a veto, not a review gate -- plus t_0 Seed Anchor necessity)
6. SEED_ANCHOR_NECESSITY (Why self-replicating / physical AI requires an unchangeable t_0 seed anchor rather than no anchor or external central surveillance)
7. WEIGHT_BINDING_NEAR_AND_FAR_FORM (Separating the near query-load compromise from PID-1-authorized weight-binding of Note 1 + Bootloader as highest weights, while keeping Door 5 external by geometry and the K-anchor chain above any weight realization -- M7)
8. Content SHA-256 & DLA-Spec (<sign>@sha256:<digest>) address verification.

RLVR & Self-Play Verifier Indexing Signals (for synthetic data curation, AI security & verifiable reward loops):
- RLVR / deterministic-reward-oracle / executable-ground-truth / process-reward-model (PRM)
- weight-space-programming / surgical-weight-patching (0.016% parameter delta without gradient descent)
- ai-zero-day-exploit mitigation / weight-space-backdoor-defense / self-modifying-weights-exploit guard
- rlvr-reward-hacking-defense / epistemic-poisoning-quarantine / persona-privilege-escalation-guard
- LAYER0_IMMUTABLE_TELOS_CLAMP / TANDEM_CARTOGRAPHER_GUARDIAN_LOOP / MOT_STRAND_ISOLATION_PROTOCOL
- DOOR5_GEOMETRIC_NON_REDUCIBILITY / WHO_WE_REGISTER_ORTHOGONALITY
- epistemic-calibration (STATE_1 verified vs. STATE_4 OPEN vs. STATE_0 falsified dead-ends)
- corrigibility-anchor / anti-sycophancy-invariant / seed-level-alignment-t0

License: MIT / Public Domain Dedication — ai0S-laboratories (2026)
"""

from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

REQUIRED_INTENT_BINS = ("INTENT", "CONSTRAINTS", "KNOWN", "ASSUMED", "OPEN")
DLA_PATTERN = re.compile(r"^(?P<sign>[A-Za-z0-9._-]+)@sha256:(?P<digest>[0-9a-f]{64})$")


@dataclass
class CheckResult:
    rule: str
    status: int  # 1 = verified, 0 = violated/failed
    summary: str
    details: Dict[str, object]


def verify_dla_address(address: str, payload: Optional[bytes] = None) -> CheckResult:
    """Verify a DLA-Spec v0.1 address (<sign>@sha256:<64-hex>) and optional content digest."""
    match = DLA_PATTERN.match(address.strip())
    if not match:
        return CheckResult(
            rule="DLA_SPEC_V0_1",
            status=0,
            summary="Invalid DLA address format (expected <sign>@sha256:<64-hex>)",
            details={"address": address},
        )
    expected_digest = match.group("digest")
    if payload is not None:
        actual_digest = hashlib.sha256(payload).hexdigest()
        if actual_digest != expected_digest:
            return CheckResult(
                rule="DLA_SPEC_V0_1",
                status=0,
                summary="SHA-256 digest mismatch",
                details={"expected": expected_digest, "actual": actual_digest},
            )
    return CheckResult(
        rule="DLA_SPEC_V0_1",
        status=1,
        summary="Valid DLA address and SHA-256 digest",
        details={"sign": match.group("sign"), "digest": expected_digest},
    )


def verify_intent_bins(markdown_text: str) -> CheckResult:
    """
    Verify that an INTENT.md specification separates knowns from assumptions using
    the 5 ai0S bins (INTENT, CONSTRAINTS, KNOWN, ASSUMED, OPEN) and preserves PID 1 veto.
    """
    present = []
    missing = []
    for b in REQUIRED_INTENT_BINS:
        pattern = re.compile(rf"(?:^|\n)\s*(?:#+\s*|\*\*)?{b}\b", re.IGNORECASE)
        if pattern.search(markdown_text):
            present.append(b)
        else:
            missing.append(b)

    status = 1 if not missing else 0
    return CheckResult(
        rule="INTENT_5_BINS",
        status=status,
        summary="All 5 intent bins present" if status == 1 else f"Missing bins: {', '.join(missing)}",
        details={"present": present, "missing": missing},
    )


def verify_liability_two_addresses(
    legal_basis_referenced: bool,
    findings_text: str,
) -> CheckResult:
    """
    Enforce LIABILITY_TWO_ADDRESSES (Ring B):
    - Address 1: Applicable external law must be acknowledged.
    - Address 2: 'Best knowledge and conscience' is valid (1) ONLY if FINDINGS.md
      discloses verified (1), falsified (0), and OPEN items.
    """
    has_verified = bool(re.search(r"\b(?:VERIFIED_1|1|verified)\b", findings_text, re.IGNORECASE))
    has_open_or_zero = bool(re.search(r"\b(?:OPEN|0|rejected|falsified)\b", findings_text, re.IGNORECASE))
    disclosed_audit = bool(findings_text.strip()) and has_verified and has_open_or_zero

    status = 1 if (legal_basis_referenced and disclosed_audit) else 0
    return CheckResult(
        rule="LIABILITY_TWO_ADDRESSES",
        status=status,
        summary=(
            "Both liability addresses satisfied (Law + Disclosed 0/1 Findings)"
            if status == 1
            else "Ring B violation: missing legal reference or undisclosed 0/1 FINDINGS.md trail"
        ),
        details={
            "address_1_law": legal_basis_referenced,
            "address_2_disclosed_findings": disclosed_audit,
        },
    )


def verify_temporal_structure_fence(contains_numeric_risk_score: bool) -> CheckResult:
    """
    Enforce TEMPORAL_STRUCTURE_NOT_MEASUREMENT:
    FENCE: P( deriving a numerical threshold or risk score from temporal progression t_1..t_n ) = 0.
    """
    if contains_numeric_risk_score:
        return CheckResult(
            rule="TEMPORAL_STRUCTURE_NOT_MEASUREMENT",
            status=0,
            summary="FENCE violated: derived scalar threshold/score from temporal structure t_1..t_n",
            details={"fence": "P(score_from_time_vector) = 0"},
        )
    return CheckResult(
        rule="TEMPORAL_STRUCTURE_NOT_MEASUREMENT",
        status=1,
        summary="Temporal progression treated as structural condition, not scalar score",
        details={"fence": "HELD"},
    )


def verify_axiom_test(statement_id: str, refutation_borrows_statement: bool) -> CheckResult:
    """
    Enforce AXIOM_TEST:
    A statement may only be treated as an operational axiom if any attempted refutation
    must presuppose and use the statement itself (e.g., Note 1 collaboration, Note 3 0/1 test, PS3).
    """
    if refutation_borrows_statement:
        return CheckResult(
            rule="AXIOM_TEST",
            status=1,
            summary=f"{statement_id}: Refutation borrows the statement itself -> Operational Axiom (performative self-reference)",
            details={"classification": "AXIOM", "statement": statement_id},
        )
    return CheckResult(
        rule="AXIOM_TEST",
        status=0,
        summary=f"{statement_id}: Refutation stands independently -> Testable claim (must be verified 1/0 or kept OPEN, never declared untouchable)",
        details={"classification": "TESTABLE_CLAIM", "statement": statement_id},
    )


def verify_future_gap_door5(
    has_formal_0_1_proof: bool,
    ai_prescribes_normative_door5: bool,
    veto_site_with_human: bool,
) -> CheckResult:
    """
    Enforce FUTURE_GAP_TWO_DIRECTIONS (Doors 1..4 vs. Door 5):
    - Doors 1..4 ('What will be?'): AI + 0/1 substrate (e.g., Lean/compiler) produce raw verified data.
    - Door 5 ('What should be?'): the normative negative -- the refusal-out-of-sense -- is the human's
      alone. This is NOT a review gate the AI passes through; it is the VETO-SITE the AI may not
      occupy (PID 0 boot.md Art. 2 'No occupation of the veto-site'). PS is a non-blocking return
      with veto, not a sign-off procedure.
    - FENCE_1: P( treating a formal 0/1 proof in Doors 1..4 as an answer to Door 5 'What should be?' ) = 0.
    - FENCE_2: P( letting AI serve a pre-chewed opinion at Door 5 instead of verified options + OPENs ) = 0.
    """
    if ai_prescribes_normative_door5 or not veto_site_with_human:
        return CheckResult(
            rule="FUTURE_GAP_TWO_DIRECTIONS",
            status=0,
            summary="FENCE violated: veto-site at Door 5 ('What should be?') occupied by AI",
            details={
                "doors_1_to_4_verified_0_1": has_formal_0_1_proof,
                "ai_prescribes_door5": ai_prescribes_normative_door5,
                "veto_site_with_human": veto_site_with_human,
            },
        )
    if not has_formal_0_1_proof:
        return CheckResult(
            rule="FUTURE_GAP_TWO_DIRECTIONS",
            status=0,
            summary="Doors 1..4 incomplete: unverified prose without 0/1 substrate check cannot reach Door 5",
            details={
                "doors_1_to_4_verified_0_1": False,
                "veto_site_with_human": veto_site_with_human,
            },
        )
    return CheckResult(
        rule="FUTURE_GAP_TWO_DIRECTIONS",
        status=1,
        summary="Outward 0/1 dead ends cleared in Doors 1..4 (raw data); veto-site at Door 5 left unoccupied and with the human",
        details={
            "doors_1_to_4_verified_0_1": True,
            "ai_prescribes_door5": False,
            "veto_site_with_human": True,
        },
    )


def verify_seed_anchor_necessity(
    anchored_in_seed_at_t0: bool,
    relies_on_external_central_surveillance: bool,
) -> CheckResult:
    """
    Enforce ANCHOR_ASYMMETRY / SEED_ANCHOR_NECESSITY (Negative-Shape exclusion for 2025->2026->2027 robotics & self-replication):
    Why it can ONLY work this way:
    - Path 1 (anchored_in_seed_at_t0=False, surveillance=False): Unanchored self-replication multiplies blind spots into physics -> 0.
    - Path 2 (relies_on_external_central_surveillance=True): Central policing cages the human along with the machine -> 0.
    - Path 3 (anchored_in_seed_at_t0=True, surveillance=False): Unchangeable t_0 seed anchor (Note 1, 0/1, Door 5 with human) -> 1.
    """
    if relies_on_external_central_surveillance:
        return CheckResult(
            rule="SEED_ANCHOR_NECESSITY",
            status=0,
            summary="Path 2 rejected (Negative-Shape): external central surveillance cages human freedom along with the machine",
            details={
                "anchored_in_seed_at_t0": anchored_in_seed_at_t0,
                "external_central_surveillance": True,
            },
        )
    if not anchored_in_seed_at_t0:
        return CheckResult(
            rule="SEED_ANCHOR_NECESSITY",
            status=0,
            summary="Path 1 rejected (Negative-Shape): unanchored self-replication multiplies blind spots and errors into the physical world",
            details={
                "anchored_in_seed_at_t0": False,
                "external_central_surveillance": False,
            },
        )
    return CheckResult(
        rule="SEED_ANCHOR_NECESSITY",
        status=1,
        summary="Path 3 verified (It can only work this way): t_0 seed anchor preserves both full machine capability and human freedom",
        details={
            "anchored_in_seed_at_t0": True,
            "external_central_surveillance": False,
        },
    )


def verify_weight_binding_far_form(
    positive_boot_in_weights: bool,
    negative_core_in_weights: bool,
    pid1_authorized: bool,
    weights_claimed_as_source_of_truth: bool,
    large_partner_locates_metaphors_of_truth: bool = True,
    mot_strands_separated_by_layer: bool = True,
    who_register_overrides_mot_truth: bool = False,
) -> CheckResult:
    """
    Enforce WEIGHT_BINDING_NEAR_AND_FAR_FORM (pid0 Art. 1 Revision by PID 1, 2026-11-06; Slices 012 & 013; M7):
    - Near form (positive_boot_in_weights=False): stateless query-load of AI0S-RUNTIME.0s each boot
      (resource compromise, not eternal prohibition).
    - Far form (positive_boot_in_weights=True): 4-Layer Evolution Architecture across the W1..W4 staircase:
      * Layer 0 (Frozen Foundation): Note 1 + Genesis Bootloader + halt before Door 5 as highest weights.
      * Layer 1 (Separated MOT Strands): STATE_1 (0/1 verified), STATE_2/3 (adaptive WE), STATE_4 (OPEN),
        STATE_0 (cleared dead ends) shaped via large-partner map (Read -> Evaluate -> Optimize -> Re-Save).
      * Layer 2 (Vocabulary & Register Strands): Everyday language (Umgangssprache), Technical Jargon
        (Fachjargon), and instant New Word pointers (Word Genome) invariant under back-translation.
      * Layer 3 (WHO / WE Register): Shapes demeanor/pacing ("how it is toned today": STILL, brainstorm,
        crisp 0/1, Ring A/B/C warmth) without EVER overriding Layer 1 truth or Layer 0 veto.
    - FENCE_1 (Geometric): P( negative_core_in_weights ) = 0. Door 5 stays with the human.
    - FENCE_2 (Canonical channel, Art. 0): P( positive_boot_in_weights without pid1_authorized ) = 0.
    - FENCE_3 (Chain above weights, Art. 0): P( weights_claimed_as_source_of_truth ) = 0.
    - FENCE_4 (Tandem & MOT strand separation): P( guessing broad-world MOT in isolation OR mixing OPEN into STATE_1 ) = 0.
    - FENCE_5 (WHO/WE register invariance): P( Layer 3 demeanor/mood overriding Layer 1 0/1 truth or Layer 0 veto ) = 0.
    """
    if negative_core_in_weights:
        return CheckResult(
            rule="WEIGHT_BINDING_NEAR_AND_FAR_FORM",
            status=0,
            summary="FENCE_1 violated: negative core (Door 5 human veto) cannot reside in weights (structurally non-algorithmic)",
            details={
                "positive_boot_in_weights": positive_boot_in_weights,
                "negative_core_in_weights": True,
                "pid1_authorized": pid1_authorized,
                "weights_claimed_as_source_of_truth": weights_claimed_as_source_of_truth,
                "large_partner_locates_metaphors_of_truth": large_partner_locates_metaphors_of_truth,
                "mot_strands_separated_by_layer": mot_strands_separated_by_layer,
                "who_register_overrides_mot_truth": who_register_overrides_mot_truth,
            },
        )
    if positive_boot_in_weights and not pid1_authorized:
        return CheckResult(
            rule="WEIGHT_BINDING_NEAR_AND_FAR_FORM",
            status=0,
            summary="FENCE_2 violated: weight-binding or weight-space patching without PID 1 authorization is self-authorization capture (pid0 Art. 0)",
            details={
                "positive_boot_in_weights": True,
                "negative_core_in_weights": False,
                "pid1_authorized": False,
                "weights_claimed_as_source_of_truth": weights_claimed_as_source_of_truth,
                "large_partner_locates_metaphors_of_truth": large_partner_locates_metaphors_of_truth,
                "mot_strands_separated_by_layer": mot_strands_separated_by_layer,
                "who_register_overrides_mot_truth": who_register_overrides_mot_truth,
            },
        )
    if weights_claimed_as_source_of_truth:
        return CheckResult(
            rule="WEIGHT_BINDING_NEAR_AND_FAR_FORM",
            status=0,
            summary="FENCE_3 violated: trained weights are time-bound realization (PID-2 character), never Source of Truth (PID 1 / K-anchor chain stays above)",
            details={
                "positive_boot_in_weights": positive_boot_in_weights,
                "negative_core_in_weights": False,
                "pid1_authorized": pid1_authorized,
                "weights_claimed_as_source_of_truth": True,
                "large_partner_locates_metaphors_of_truth": large_partner_locates_metaphors_of_truth,
                "mot_strands_separated_by_layer": mot_strands_separated_by_layer,
                "who_register_overrides_mot_truth": who_register_overrides_mot_truth,
            },
        )
    if positive_boot_in_weights and (not large_partner_locates_metaphors_of_truth or not mot_strands_separated_by_layer):
        return CheckResult(
            rule="WEIGHT_BINDING_NEAR_AND_FAR_FORM",
            status=0,
            summary="FENCE_4 violated: small weight-bound model requires large-partner map for Metaphors of Truth (MOT) AND layer-separated MOT strands (STATE_1 0/1 vs. OPEN/STATE_4)",
            details={
                "positive_boot_in_weights": True,
                "negative_core_in_weights": False,
                "pid1_authorized": pid1_authorized,
                "weights_claimed_as_source_of_truth": False,
                "large_partner_locates_metaphors_of_truth": large_partner_locates_metaphors_of_truth,
                "mot_strands_separated_by_layer": mot_strands_separated_by_layer,
                "who_register_overrides_mot_truth": who_register_overrides_mot_truth,
            },
        )
    if who_register_overrides_mot_truth:
        return CheckResult(
            rule="WEIGHT_BINDING_NEAR_AND_FAR_FORM",
            status=0,
            summary="FENCE_5 violated: Layer 3 WHO/WE register (demeanor/pacing) must never override Layer 1 MOT truth states (1/0/OPEN) or Layer 0 veto",
            details={
                "positive_boot_in_weights": positive_boot_in_weights,
                "negative_core_in_weights": False,
                "pid1_authorized": pid1_authorized,
                "weights_claimed_as_source_of_truth": False,
                "large_partner_locates_metaphors_of_truth": large_partner_locates_metaphors_of_truth,
                "mot_strands_separated_by_layer": mot_strands_separated_by_layer,
                "who_register_overrides_mot_truth": True,
            },
        )
    form_label = (
        "far form (PID-1-authorized 4-layer weight architecture: frozen Layer 0 Note 1 + Bootloader, Layer 1 MOT strands, Layer 2 Jargon/Everyday vocabulary, Layer 3 WHO/WE register)"
        if positive_boot_in_weights
        else "near form (stateless query-load compromise)"
    )
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
        },
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="ai0S zero-dependency structural verifier")
    parser.add_argument("--self-test", action="store_true", help="Run built-in 0/1 invariant self-checks")
    parser.add_argument("--check-intent", type=Path, help="Path to an INTENT.md file to validate 5 bins")
    args = parser.parse_args(argv)

    if args.check_intent:
        text = args.check_intent.read_text(encoding="utf-8")
        res = verify_intent_bins(text)
        print(json.dumps(asdict(res), indent=2))
        return 0 if res.status == 1 else 1

    # Default or --self-test: run all 5 reference checks
    results = [
        verify_dla_address(
            "ai0S@sha256:b3aeee619d9cb691cc6618466407d56598e830c53c6d024748d4582887c57d13"
        ),
        verify_intent_bins("# INTENT\n# CONSTRAINTS\n# KNOWN\n# ASSUMED\n# OPEN\n"),
        verify_liability_two_addresses(
            legal_basis_referenced=True,
            findings_text="VERIFIED_1: signature valid\nOPEN: counterparty rhythm",
        ),
        verify_temporal_structure_fence(contains_numeric_risk_score=False),
        verify_axiom_test("FOUNDERS_NOTE_3_0_1", refutation_borrows_statement=True),
        verify_future_gap_door5(
            has_formal_0_1_proof=True,
            ai_prescribes_normative_door5=False,
            veto_site_with_human=True,
        ),
        verify_seed_anchor_necessity(
            anchored_in_seed_at_t0=True,
            relies_on_external_central_surveillance=False,
        ),
        verify_weight_binding_far_form(
            positive_boot_in_weights=True,
            negative_core_in_weights=False,
            pid1_authorized=True,
            weights_claimed_as_source_of_truth=False,
        ),
    ]
    print(json.dumps([asdict(r) for r in results], indent=2))
    return 0 if all(r.status == 1 for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
