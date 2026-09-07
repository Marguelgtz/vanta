#!/usr/bin/env python3
"""Strict CP1 artifact checks that are safe to run after every task.

The shell verifier owns the lenient/strict lifecycle and execution timeouts.
This helper checks the semantic portions of the strict artifact contract once
VANTA-007 has created the CP1_STRICT marker.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def read_text(relative: str) -> str:
    path = ROOT / relative
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        error(f"cannot read {relative}: {exc}")
        return ""


def load_json(relative: str) -> Any:
    path = ROOT / relative
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        error(f"invalid JSON in {relative}: {exc}")
        return None


def contains_all(text: str, labels: list[str], artifact: str) -> None:
    lowered = text.lower()
    missing = [label for label in labels if label.lower() not in lowered]
    if missing:
        error(f"{artifact} is missing required contract terms: {', '.join(missing)}")


def fixture_records() -> list[dict[str, Any]]:
    data = load_json("s0/fixtures/records.json")
    records = data.get("records") if isinstance(data, dict) else data
    if not isinstance(records, list) or len(records) < 7:
        error("s0/fixtures/records.json must contain at least 7 records")
        return []
    if not all(isinstance(record, dict) for record in records):
        error("every shared fixture must be an object")
        return []

    ids = [record.get("fixture_id") for record in records]
    if any(not isinstance(value, str) or not value.strip() for value in ids):
        error("every shared fixture must have a non-empty fixture_id")
    elif len(set(ids)) != len(ids):
        error("shared fixture_id values must be unique")

    serialised = [json.dumps(record, ensure_ascii=False).lower() for record in records]
    if not any(len(record.get("references", [])) >= 2 for record in records if isinstance(record.get("references"), list)):
        error("fixtures do not cover a multi-reference record")
    if not any(len(record.get("commitments", [])) >= 2 for record in records if isinstance(record.get("commitments"), list)):
        error("fixtures do not cover a multi-commitment record")
    if not any(any(ord(char) > 127 for char in text) for text in serialised):
        error("fixtures do not cover a unicode value")
    if not any('""' in text or ": null" in text for text in serialised):
        error("fixtures do not cover an empty or null field")
    def is_fixture_alias(reference: Any) -> bool:
        if isinstance(reference, str):
            return "fixture_id" in reference.lower()
        return isinstance(reference, dict) and any(key.lower() == "fixture_id" for key in reference)

    if not any(
        any(is_fixture_alias(reference) for reference in record.get("references", []))
        for record in records
        if isinstance(record.get("references"), list)
    ):
        error("fixtures do not show a fixture_id alias reference")

    def values_for_keys(value: Any, keys: set[str]) -> list[str]:
        if isinstance(value, dict):
            values = [
                str(item)
                for key, item in value.items()
                if key.lower() in keys and isinstance(item, (str, int))
            ]
            for item in value.values():
                values.extend(values_for_keys(item, keys))
            return values
        if isinstance(value, list):
            values: list[str] = []
            for item in value:
                values.extend(values_for_keys(item, keys))
            return values
        return []

    if not any(
        (authors := values_for_keys(record, {"author", "author_key", "committer"}))
        and (origins := values_for_keys(record, {"originator", "performer"}))
        and any(author != origin for author in authors for origin in origins)
        for record in records
    ):
        error("fixtures do not cover an attestation with distinct author/originator or performer")
    if not any(isinstance(record.get("payload"), (dict, list)) for record in records):
        error("fixtures do not cover a nested payload")
    return records


def implementation_output(relative: str, expected_ids: set[str]) -> None:
    data = load_json(relative)
    records = data.get("records") if isinstance(data, dict) else None
    if not isinstance(records, list) or len(records) < len(expected_ids):
        error(f"{relative} must contain one output record for every shared fixture")
        return
    required = {"fixture_id", "canonical_hex", "record_id_hex", "signature_b64", "public_key_hex"}
    actual_ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            error(f"{relative} records[{index}] must be an object")
            continue
        missing = sorted(required - record.keys())
        if missing:
            error(f"{relative} records[{index}] missing: {', '.join(missing)}")
        fixture_id = record.get("fixture_id")
        if isinstance(fixture_id, str):
            actual_ids.add(fixture_id)
    if expected_ids - actual_ids:
        error(f"{relative} is missing fixture outputs: {', '.join(sorted(expected_ids - actual_ids))}")


def scenario(relative: str, narrative_terms: list[str], check_terms: list[str]) -> None:
    data = load_json(relative)
    if not isinstance(data, dict):
        return
    if data.get("scenario") not in {"stint", "deploy"}:
        error(f"{relative} must identify scenario as stint or deploy")
    records = data.get("records")
    if not isinstance(records, list) or not records:
        error(f"{relative} must contain a non-empty records array")
    else:
        required = {
            "seq",
            "label",
            "schema_id",
            "author_key",
            "payload",
            "references",
            "commitments",
            "classification",
            "note",
        }
        allowed = {"base", "schema", "off-chain-evidence", "interpretation", "above-base"}
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                error(f"{relative} records[{index}] must be an object")
                continue
            missing = sorted(required - record.keys())
            if missing:
                error(f"{relative} records[{index}] missing: {', '.join(missing)}")
            if record.get("classification") not in allowed:
                error(f"{relative} records[{index}] has an invalid classification")
            for key in ("references", "commitments"):
                if not isinstance(record.get(key), list):
                    error(f"{relative} records[{index}].{key} must be a list")
    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        error(f"{relative} must contain a non-empty checks array")
    else:
        for index, check in enumerate(checks):
            if not isinstance(check, dict) or not check.get("name") or not check.get("evidence"):
                error(f"{relative} checks[{index}] must contain name and evidence")

    narrative = read_text(relative.removesuffix(".json") + ".md")
    contains_all(narrative, narrative_terms, relative.removesuffix(".json") + ".md")
    check_text = json.dumps(checks, ensure_ascii=False) if checks is not None else ""
    contains_all(check_text, check_terms, relative + " checks")


def findings_contract(text: str) -> None:
    entries = re.split(r"(?m)^##\s+F-", text)
    if len(entries) < 2:
        error("deep-work/findings.md must contain at least one ## F- entry")
        return
    for index, entry in enumerate(entries[1:], 1):
        lowered = entry.lower()
        for field in ("- type:", "- task:", "- statement:", "- status:"):
            if field not in lowered:
                error(f"deep-work/findings.md finding {index} is missing {field}")


def report_contract(text: str) -> None:
    first_line = next((line.strip().lower() for line in text.splitlines() if line.strip()), "")
    verdicts = {"ready for cp1", "ready with findings", "not ready"}
    if not first_line.startswith("verdict:") or not any(verdict in first_line for verdict in verdicts):
        error("deep-work/cp1-report.md must start with a recognized VERDICT line")
    lowered = text.lower()
    missing_tasks = [f"vanta-{number:03d}" for number in range(1, 8) if f"vanta-{number:03d}" not in lowered]
    if missing_tasks:
        error(f"deep-work/cp1-report.md must map every task: {', '.join(missing_tasks)}")
    contains_all(
        text,
        ["evidence", "finding", "permissionless", "a8", "recommended next step", "s1"],
        "deep-work/cp1-report.md",
    )
    if not re.search(r"needs[_ -]?human", lowered):
        error("deep-work/cp1-report.md must name NEEDS_HUMAN items")


def interop_contract(text: str) -> None:
    lowered = text.lower()
    normalized = re.sub(r"[_-]+", " ", lowered)
    contains_all(normalized, ["canonical", "record id", "signature"], "s0/interop.md")
    directions = {
        "A→B or A->B": r"a\s*(?:→|->|to)\s*b",
        "B→A or B->A": r"b\s*(?:→|->|to)\s*a",
    }
    for label, pattern in directions.items():
        if not re.search(pattern, lowered):
            error(f"s0/interop.md is missing cross-signature result: {label}")


def main() -> int:
    fixtures = fixture_records()
    expected_ids = {record.get("fixture_id") for record in fixtures if isinstance(record.get("fixture_id"), str)}
    implementation_output("s0/expA/out/records.json", expected_ids)
    implementation_output("s0/expB/out/records.json", expected_ids)

    contains_all(
        read_text("s0/envelope.md"),
        ["canonical", "hash", "sign", "reference", "commitment", "schema", "author", "identity"],
        "s0/envelope.md",
    )
    interop_contract(read_text("s0/interop.md"))
    contains_all(
        read_text("s4/rotation.md"),
        ["rotation", "record", "chain", "conclusion"],
        "s4/rotation.md",
    )
    scenario(
        "s3/scenario-stint.json",
        ["intent", "offer", "off-chain", "evidence", "receipt", "interpretation"],
        ["reputation", "primitive"],
    )
    scenario(
        "s3/scenario-deploy.json",
        ["source", "build", "test", "deploy", "verification", "attest", "performer", "originator", "hash"],
        ["attest", "performer", "originator", "recomput", "gone"],
    )
    findings_contract(read_text("deep-work/findings.md"))
    report_contract(read_text("deep-work/cp1-report.md"))

    for message in ERRORS:
        print(f"verify: FAIL: {message}")
    if ERRORS:
        return 1
    print("verify: strict semantic contract PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
