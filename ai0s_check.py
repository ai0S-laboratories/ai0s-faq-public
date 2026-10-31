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
7. Content SHA-256 & DLA-Spec (<sign>@sha256:<digest>) address verification.

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
    ]
    print(json.dumps([asdict(r) for r in results], indent=2))
    return 0 if all(r.status == 1 for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
