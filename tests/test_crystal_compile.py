import json
import unittest
from pathlib import Path
import sys

CLI_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CLI_DIR))

import crystal_compile  # noqa: E402


class TestCrystalCompiler(unittest.TestCase):
    def test_example_ledger_compiles_zero_ghost_traces_and_seals_ring_a(self) -> None:
        ledger = CLI_DIR / "example.crystal.jsonl"
        records = crystal_compile.load_crystal_ledger(ledger)
        manifest = crystal_compile.compile_clean_strands(records, allow_ring_a=False)

        self.assertEqual(manifest["ghost_trace_count"], 0)
        self.assertEqual(manifest["superseded_revisions_purged"], 2)
        self.assertEqual(manifest["ring_a_withheld_count"], 1)

        # CRYSTAL-001 moved OPEN+ -> STATE_1_VERIFIED: must ONLY exist in STATE_1_VERIFIED
        open_plus_ids = [e["crystal_id"] for e in manifest["strands"]["STATE_4_OPEN_PLUS"]]
        verified_ids = [e["crystal_id"] for e in manifest["strands"]["STATE_1_VERIFIED"]]
        self.assertNotIn("CRYSTAL-001", open_plus_ids)
        self.assertIn("CRYSTAL-001", verified_ids)

        # CRYSTAL-002 moved OPEN- -> STATE_0_EXCLUDED: must ONLY exist in STATE_0_EXCLUDED
        open_minus_ids = [e["crystal_id"] for e in manifest["strands"]["STATE_4_OPEN_MINUS"]]
        excluded_ids = [e["crystal_id"] for e in manifest["strands"]["STATE_0_EXCLUDED"]]
        self.assertNotIn("CRYSTAL-002", open_minus_ids)
        self.assertIn("CRYSTAL-002", excluded_ids)

        # Ring A (CRYSTAL-004) must never appear in public/shared strands
        all_public_ids = [
            e["crystal_id"]
            for bucket in manifest["strands"].values()
            for e in bucket
        ]
        self.assertNotIn("CRYSTAL-004", all_public_ids)

    def test_normative_door5_prescription_is_rejected(self) -> None:
        bad_record = {
            "crystal_id": "BAD-001",
            "revision": 1,
            "timestamp": "2026-11-14T10:00:00Z",
            "ring": "C",
            "mot_state": "STATE_1_VERIFIED",
            "shell2_term": "telos_override",
            "claim_0_1": "Prescribe human life meaning automatically.",
            "evidence_anchor": "none",
            "prescribes_door5_normative_choice": True,
        }
        with self.assertRaises(crystal_compile.CrystalCompileError):
            crystal_compile.compile_clean_strands([bad_record])


if __name__ == "__main__":
    unittest.main()
