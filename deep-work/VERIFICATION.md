# Vanta CP1 — verification contract

Read this before producing any artifact. The layout below is the single source of truth
for where evidence goes; `scripts/verify-cp1` checks exactly this contract.

## Verification modes

- **LENIENT (default):** whatever artifacts *exist* must be valid; artifacts belonging to
  later tasks may be absent. Stint runs the verification command after every task
  attempt, so a task must never fail because a *later* task's artifacts do not exist yet
  (live-run lesson, Stint `DEEP_WORK.md` §8).
- **STRICT:** the full CP1 artifact set is required. Activated by the marker file
  `deep-work/state/CP1_STRICT` (created only in VANTA-007) or `STRICT_OVERRIDE=1`
  (local testing). In strict mode, `scripts/verify-cp1` also runs
  `scripts/verify-cp1-strict.py`, which checks the semantic portions of this
  contract rather than only file presence and top-level JSON shape.

Budgets: Stint caps mission-level verification at 3 minutes; the script caps each
implementation's test run at 80 s.

## Per-task verification

Stint runs each task's own `verify:` command (defined under the task in
`CP1_MISSION.md`) after every attempt of that task; only tasks without a `verify:`
fall back to the mission-level `bash scripts/verify-cp1`. Because the cumulative
verifier passes (lenient) on an empty worktree, every task carries a scoped command
so a task can never be VERIFIED on the mere exit-0 of the cumulative check:

| Task | Per-task `verify:` (run in the worktree, 3-minute cap) |
|---|---|
| VANTA-001 | `test -s s0/envelope.md && test -s deep-work/findings.md && test -s s0/fixtures/records.json && bash scripts/verify-cp1` |
| VANTA-002 | `test -x s0/expA/test && test -s s0/expA/out/records.json && bash scripts/verify-cp1` |
| VANTA-003 | `test -x s0/expB/test && test -s s0/expB/out/records.json && test -s s0/interop.md && bash scripts/verify-cp1` |
| VANTA-004 | `test -s s3/scenario-stint.md && test -s s3/scenario-stint.json && bash scripts/verify-cp1` |
| VANTA-005 | `test -s s3/scenario-deploy.md && test -s s3/scenario-deploy.json && bash scripts/verify-cp1` |
| VANTA-006 | `test -s s4/rotation.md && bash scripts/verify-cp1` |
| VANTA-007 | `test -f deep-work/state/CP1_STRICT && test -s deep-work/cp1-report.md && bash scripts/verify-cp1` |

Each command ends in the lenient cumulative check (validates whatever exists), so a
task still cannot false-fail on a later task's missing artifacts; the leading `test`
clauses pin VERIFIED to the task's own artifacts. VANTA-007's command runs in strict
mode because by then `deep-work/state/CP1_STRICT` exists and the report is written.

## Artifact map

| Path | Created by | Contract |
|---|---|---|
| `deep-work/findings.md` | every task, append-only | `## F-<n> <date> — <title>` entries: `- type: choice \| finding \| gap \| NEEDS_HUMAN`, `- task: VANTA-00x`, `- statement: …`; gap entries additionally carry the 5-question change-gate answers and `- status: open \| resolved \| NEEDS_HUMAN` |
| `s0/envelope.md` | VANTA-001 | the canonical form: field order + encodings; exactly which bytes are hashed (record ID); exactly which bytes are signed; how `references[]`/`commitments[]` are normalized; how `schema_id` binds the payload; and a statement that the record's author (signer) is the only protocol-level identity, originator/performer/attester being schema-level payload concepts (MVP_PLAN §4 Actor, §3) |
| `s0/fixtures/records.json` | VANTA-001 | language-neutral logical records, ≥ 7, covering: minimal record; multi-reference; multi-commitment; unicode + empty fields; nested payload; a record referencing an earlier fixture by `fixture_id` alias; an attestation signed by author A whose schema-level originator/performer field names a *different* actor O (O ≠ committer, referencing an earlier fixture) |
| `s0/expA/`, `s0/expB/` | VANTA-002 / 003 | self-contained implementation; MUST ship an executable `test` script that runs the full suite (and, for expB, the interop check) and exits 0 when green |
| `s0/expA/out/records.json`, `s0/expB/out/records.json` | VANTA-002 / 003 | `{"records":[{"fixture_id","canonical_hex","record_id_hex","signature_b64","public_key_hex"}]}` — consumed by the other implementation's interop check |
| `s0/interop.md` | VANTA-003 | interop evidence: byte-identity of canonical bytes, record-ID identity, cross signature verification results (A→B and B→A) |
| `s3/scenario-stint.md` + `s3/scenario-stint.json` | VANTA-004 | Scenario A paper-walk (MVP_PLAN §7): narrative + classification table, machine-checkable JSON (below) |
| `s3/scenario-deploy.md` + `s3/scenario-deploy.json` | VANTA-005 | Scenario B paper-walk (MVP_PLAN §7): same shape, plus the explicit Scenario-B checks |
| `s4/rotation.md` | VANTA-006 | S4 convention + demonstration-or-argument + conclusion on protocol-machinery cost |
| `deep-work/cp1-report.md` | VANTA-007 | `VERDICT: READY FOR CP1` / `VERDICT: READY WITH FINDINGS` / `VERDICT: NOT READY`; evidence table (each Success criterion → artifact/test); findings summary; NEEDS_HUMAN list; recommended next step |
| `deep-work/state/CP1_STRICT` | VANTA-007 | empty marker file; switches verification to strict |

## Scenario JSON contract (validated by the script)

```json
{
  "scenario": "stint | deploy",
  "records": [
    {
      "seq": 1,
      "label": "human-readable step label",
      "schema_id": "hex, or an alias defined in the .md",
      "author_key": "hex, or an alias",
      "payload": "sketch, or a pointer to the payload description",
      "references": ["record id or alias"],
      "commitments": ["content hash or alias"],
      "classification": "base | schema | off-chain-evidence | interpretation | above-base",
      "note": "free text"
    }
  ],
  "checks": [ { "name": "…", "evidence": "…" } ]
}
```

Required: top-level `records` non-empty; every record has `schema_id`, `author_key`,
`references` (list), `commitments` (list). Canonical bytes/IDs may be filled in from
expA/expB where available; aliases are acceptable when an implementation is not yet
available (say so in the .md).

Strict mode additionally requires at least seven uniquely identified shared fixtures
covering the listed edge cases, complete scenario record fields and allowed
classifications, one output record for every fixture from each implementation, and
the documented cross-signature directions in `s0/interop.md`. It checks that the
envelope, rotation convention, findings entries, and final report contain their
required sections. The final report must name A8/permissionless contribution and
the recommended next step so an unresolved human gate cannot disappear behind a
generic READY verdict.

## Findings and report formats

```
## F-1 2026-02-09 — Chose Node.js + Python 3.12 as the S0 language pair
- type: choice
- task: VANTA-001
- statement: …toolchain probe evidence…
- status: resolved
```

CP1 report: verdict line first, then the evidence table, then findings with
classifications, then NEEDS_HUMAN items, then the recommended next step (S1).
