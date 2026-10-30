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


if __name__ == "__main__":
    unittest.main()
