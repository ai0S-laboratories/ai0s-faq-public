#!/usr/bin/env python3
"""
crystal_compile.py — Zero-dependency reference compiler for ai0S 2D Knowledge Crystals.

Demonstrates and enforces SOURCE_REGISTER_TO_WEIGHT_COMPILATION (FENCE_II_7):
- Appends/reads timestamped 2D crystal records (`content_pointer x MOT_state x Ring_scope`)
  from a JSONL ledger (e.g. `example.crystal.jsonl`).
- Compiles clean, disjoint Shell 1 MOT strands (`STATE_1_VERIFIED`, `STATE_2_3_CONTEXTUAL`,
  `STATE_4_OPEN_PLUS`, `STATE_4_OPEN_MINUS`, `STATE_0_EXCLUDED`) strictly from the latest
  authoritative state per `crystal_id`.
- Guarantees ZERO ghost traces (`ghost_trace_count == 0`): when an entry transitions from
  `STATE_4_OPEN_*` to `STATE_1_VERIFIED` or `STATE_0_EXCLUDED`, all superseded revisions
  vanish completely from active Shell 1 training/routing strands while remaining auditable
  in the source ledger.
- Enforces `P(Ring_A_Egress) = 0`: any crystal marked `ring="A"` is excluded from shared/public
  strand compilation by geometric invariant.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

VALID_MOT_STATES = {
    "STATE_1_VERIFIED",
    "STATE_2_3_CONTEXTUAL",
    "STATE_4_OPEN_PLUS",
    "STATE_4_OPEN_MINUS",
    "STATE_0_EXCLUDED",
}

VALID_RINGS = {"A", "B", "C"}


class CrystalCompileError(ValueError):
    """Raised when a 2D crystal record violates structural 0/1 invariants."""


def validate_record(rec: Dict[str, Any], line_no: int = 0) -> None:
    required = ("crystal_id", "revision", "timestamp", "ring", "mot_state", "shell2_term", "claim_0_1", "evidence_anchor")
    missing = [k for k in required if k not in rec]
    if missing:
        raise CrystalCompileError(f"Line {line_no}: missing required fields {missing}")
    if not isinstance(rec["revision"], int) or rec["revision"] < 1:
        raise CrystalCompileError(f"Line {line_no}: revision must be integer >= 1")
    if rec["ring"] not in VALID_RINGS:
        raise CrystalCompileError(f"Line {line_no}: invalid ring {rec['ring']!r} (expected A, B, or C)")
    if rec["mot_state"] not in VALID_MOT_STATES:
        raise CrystalCompileError(f"Line {line_no}: invalid mot_state {rec['mot_state']!r}")
    if rec.get("prescribes_door5_normative_choice") is True:
        raise CrystalCompileError(f"Line {line_no}: P(normative_door5_prescription)=0 violated in crystal {rec['crystal_id']}")


def load_crystal_ledger(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for idx, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        rec = json.loads(line)
        validate_record(rec, idx)
        records.append(rec)
    return records


def compile_clean_strands(
    records: Iterable[Dict[str, Any]],
    *,
    allow_ring_a: bool = False,
) -> Dict[str, Any]:
    """
    Compile clean, ghost-free Shell 1 MOT strands from an append-only 2D crystal ledger.

    Returns a deterministic manifest containing:
    - disjoint strand buckets (`strands`)
    - superseded revision audit (`superseded_revisions_purged`)
    - Ring A egress fence counter (`ring_a_withheld_count`)
    - `ghost_trace_count` (guaranteed 0)
    - `manifest_sha256` over the compiled strands
    """
    latest_by_id: Dict[str, Dict[str, Any]] = {}
    history_by_id: Dict[str, List[Tuple[int, str]]] = {}

    for idx, rec in enumerate(records, start=1):
        validate_record(rec, idx)
        cid = str(rec["crystal_id"])
        rev = int(rec["revision"])
        history_by_id.setdefault(cid, [])
        if any(prev_rev == rev for prev_rev, _ in history_by_id[cid]):
            raise CrystalCompileError(f"Duplicate revision {rev} for crystal_id {cid!r}")
        history_by_id[cid].append((rev, rec["mot_state"]))

        prev = latest_by_id.get(cid)
        if prev is None or rev > int(prev["revision"]):
            latest_by_id[cid] = rec

    strands: Dict[str, List[Dict[str, Any]]] = {state: [] for state in sorted(VALID_MOT_STATES)}
    ring_a_withheld = 0
    superseded_purged = 0

    for cid in sorted(latest_by_id):
        history = sorted(history_by_id[cid], key=lambda item: item[0])
        if len(history) > 1:
            superseded_purged += len(history) - 1

        active = latest_by_id[cid]
        if active["ring"] == "A" and not allow_ring_a:
            ring_a_withheld += 1
            continue

        compiled_entry = {
            "crystal_id": cid,
            "active_revision": active["revision"],
            "ring": active["ring"],
            "mot_state": active["mot_state"],
            "shell2_term": active["shell2_term"],
            "claim_0_1": active["claim_0_1"],
            "evidence_anchor": active["evidence_anchor"],
        }
        strands[active["mot_state"]].append(compiled_entry)

    # Verify disjointness & zero ghost traces across all compiled strands
    seen_ids: Dict[str, str] = {}
    ghost_traces = 0
    for state, entries in strands.items():
        for entry in entries:
            cid = entry["crystal_id"]
            if cid in seen_ids:
                ghost_traces += 1
            seen_ids[cid] = state
            # Ensure no superseded state of cid survived anywhere
            active_state = latest_by_id[cid]["mot_state"]
            if state != active_state:
                ghost_traces += 1

    canonical_payload = json.dumps(strands, sort_keys=True, separators=(",", ":")).encode("utf-8")
    manifest_sha256 = hashlib.sha256(canonical_payload).hexdigest()

    return {
        "schema": "ai0s.strand_manifest/v1",
        "compiler_mode": "FRESH_FROM_2D_SOURCE_REGISTER",
        "allow_ring_a_egress": bool(allow_ring_a),
        "total_unique_crystals": len(latest_by_id),
        "superseded_revisions_purged": superseded_purged,
        "ring_a_withheld_count": ring_a_withheld,
        "ghost_trace_count": ghost_traces,
        "manifest_sha256": manifest_sha256,
        "strands": strands,
    }


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile ghost-free Shell 1 MOT strands from a 2D crystal JSONL register."
    )
    parser.add_argument(
        "ledger",
        nargs="?",
        default=str(Path(__file__).resolve().parent / "example.crystal.jsonl"),
        help="Path to *.crystal.jsonl ledger (default: bundled example.crystal.jsonl).",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in 0/1 invariant checks on the bundled example.crystal.jsonl ledger.",
    )
    args = parser.parse_args(argv)

    ledger_path = Path(args.ledger)
    records = load_crystal_ledger(ledger_path)
    manifest = compile_clean_strands(records, allow_ring_a=False)

    if args.self_test:
        ok = (
            manifest["ghost_trace_count"] == 0
            and manifest["ring_a_withheld_count"] >= 1
            and manifest["superseded_revisions_purged"] >= 2
            and all(
                e["ring"] != "A"
                for bucket in manifest["strands"].values()
                for e in bucket
            )
        )
        summary = {
            "status": 1 if ok else 0,
            "result": "VERIFIED_1" if ok else "VIOLATION_0",
            "ghost_trace_count": manifest["ghost_trace_count"],
            "superseded_revisions_purged": manifest["superseded_revisions_purged"],
            "ring_a_withheld_count": manifest["ring_a_withheld_count"],
            "manifest_sha256": manifest["manifest_sha256"],
        }
        print(json.dumps(summary, indent=2))
        return 0 if ok else 1

    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
