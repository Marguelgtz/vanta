# Vanta MVP run — base reference implementation (substrate-agnostic)

## Objective

Build Vanta's base as a working reference implementation: the record format,
canonical serialization, content IDs, and signature envelope from the CP1
evidence (`s0/envelope.md`, fixtures), plus the Actor/Schema/Record/History
primitives, a standalone third-party verifier, and both pressure-test scenarios
running end-to-end against a local test history — with a chosen substrate
boundary documented as a thin interface (A1) that the real substrate decision
(S1, after CP1+CP2) can fill in without rework.

Governing documents — read before working: `research/MVP_PLAN.md` (especially
§2 invariants I1–I9, §3 facts vs attestations, §4 primitives, §5 MVP boundary,
§10 order of work, §10 change gate, §11 definition of success) and
`deep-work/VERIFICATION.md`. If CP1 artifacts exist (`s0/`, `s3/`, `s4/`,
`deep-work/findings.md`, `deep-work/cp1-report.md`), they are the starting
point: consume them, do not redo them. If they are absent, VANTA-M-001 below
produces the minimal envelope spec + fixtures first.

This run builds code and documentation. It does NOT choose a production
substrate (S1 is CP2, after human review), does not build any value/economics
layer, and does not connect to any external network: the "shared history" in
this run is a local, append-only, permissionless test history (a file or
in-memory log) behind a small interface, so every substrate question stays
explicit and deferred.

When evidence challenges the base (invariants, primitives, the facts/attestations
split): record a finding in `deep-work/findings.md`, run the 5-question change
gate (MVP_PLAN §10), mark base-affecting findings `NEEDS_HUMAN`, and continue
independent safe work. You never resolve base-level questions yourself.

## Success
- `base/` contains a reference implementation of the four primitives (Actor/Schema/Record/History) with canonical serialization and content IDs byte-compatible with the CP1 envelope spec (when CP1 artifacts exist; otherwise with the spec produced by VANTA-M-001)
- `base/verifier/` is a standalone verifier (independent of the reference implementation's non-base code paths — it consumes public data only: records, signatures, schema definitions, history) that validates any record (signature, typing, references, inclusion/order) and reconstructs any derivation chain
- Both pressure-test scenarios (MVP_PLAN §7) run end-to-end as minimal test-consumer apps against the local test history, and the independent verifier validates the full history from public data alone
- Originator-independence is demonstrated: with the scenario originator's "services" (its process/state) stopped or removed, the independent verifier still validates the history and reconstructs the derivation chains
- Interpretation freedom is demonstrated: at least two independent interpretation programs (e.g. an audit-log view and a provenance/reputation-free summary view) compute different, correctly derived interpretations from the same history; neither interpretation is stored by the base
- Economic neutrality: nothing in `base/`, the scenarios, or the verifiers touches tokens, escrow, stake, settlement, fees, or value transfer (contamination watch-list check in `deep-work/mvp-report.md`)
- `deep-work/mvp-report.md` exists: a report mapping every §11 definition-of-success sub-criterion to its evidence, listing every finding with its change-gate classification, NEEDS_HUMAN items, and the explicit list of substrate-boundary decisions deferred to S1
- `bash scripts/verify-mvp` passes

## Constraints
- Rigid: invariants I1–I9, the facts/attestations split, and the Actor/Schema/Record/History primitive set (MVP_PLAN §2–4). Never modify these silently; challenge them only via findings + change gate + NEEDS_HUMAN.
- Substrate-neutral: NO production substrate dependency (no EVM/Solana/Cosmos/Celestia packages, no chain nodes, no network I/O). The history is a local append-only test history behind `base/history.go`-shaped interface (or the chosen-language equivalent); every place the real substrate would be involved is an explicit, named boundary in the code and the report.
- No economics anywhere in base artifacts (MVP_PLAN §5 exclusions): no token, escrow, stake, slashing, settlement, fees, or value transfer.
- No Stint ontology as Vanta vocabulary: intent/commitment/receipt/settlement/dispute/provider/consumer/verifier/reputation are schema-level payload concepts in the scenario docs — never base primitives.
- Permissionless contribution is a hard requirement (A8): the test history interface must admit append by any actor key with no registration, operator, or permission step.
- Two independent implementations where CP1 established them: keep the CP1 interop property alive in the MVP — the verifier must be able to validate records produced by a different implementation (or the same spec via an independent code path); do not let the reference implementation and the verifier share non-base code.
- Each implementation stays small and self-contained (target: reference implementation + tests ≤ ~800 lines per program; standard library or one well-known pure crypto/serialization library; no frameworks).
- Do not modify existing `research/` documents; new artifacts go in the layout defined by `deep-work/VERIFICATION.md` plus `base/` and `scenarios/` as named in the tasks.
- Test budget: every test entrypoint used by a `verify:` command must finish in under 120 s so mission verification stays inside Stint's 3-minute cap; keep individual test runs under that with a `timeout` inside the entrypoint.
- Reversible ordinary choices (language, file layout, naming, data structures) are yours to make; record each as a finding in `deep-work/findings.md`. Ontology- or production-defining choices are findings + change gate, never silent.

## Verification
bash scripts/verify-mvp

## Tasks
- [ ] VANTA-M-001: Base envelope — spec consolidation or bootstrap
  - acceptance: if CP1 artifacts exist, `base/envelope.md` is the consolidated normative envelope spec (canonical form, hashed/signed bytes, record ID derivation, references/commitments normalization, schema binding, author-only protocol identity) with a section recording every CP1 finding that shaped it and every deviation (each deviation = a change-gate finding); if CP1 artifacts are absent, `base/envelope.md` is a fresh minimal spec plus `base/fixtures/records.json` with >= 7 language-neutral records covering the CP1 fixture set; `bash scripts/verify-mvp` passes
  - verify: test -s base/envelope.md && bash scripts/verify-mvp
- [ ] VANTA-M-002: Reference implementation (base primitives)
  - acceptance: `base/` implements Actor (key model + rotation chain), Schema (publish/resolve/evolve by ID), Record (canonical serialization + content ID + Ed25519 sign/verify), History (local append-only permissionless test history with ordering) per the envelope spec; `./base/test` (an executable entrypoint, timeout-capped) passes and covers determinism, equivalent-logical-records, references/commitments normalization, sign/verify round-trip, schema resolve, rotation continuity, and ordering; `bash scripts/verify-mvp` passes
  - verify: test -x base/test && bash scripts/verify-mvp
- [ ] VANTA-M-003: Standalone third-party verifier
  - acceptance: `base/verifier/` is an independent verification program consuming public data only (records, signatures, schema definitions, the history) — no shared non-base code with the VANTA-M-002 implementation; `./base/verifier/test` (executable, timeout-capped) passes and covers: validation of well-formed records, rejection of bad signatures, rejection of broken references, rejection of ordering violations, and reconstruction of a derivation chain from history alone; `bash scripts/verify-mvp` passes
  - verify: test -x base/verifier/test && bash scripts/verify-mvp
- [ ] VANTA-M-004: Scenario A end-to-end (Stint-shaped, MVP_PLAN §7)
  - acceptance: `scenarios/stint/` is a minimal test-consumer app that runs the full Scenario A record sequence (intent → offer → off-chain work → evidence commitments → receipt → interpretation) against the local test history using the base primitives; `./scenarios/stint/test` (executable, timeout-capped) runs the scenario, then runs the VANTA-M-003 independent verifier over the resulting history and passes only if the verifier accepts every record and reconstructs the derivation chain; the scenario's domain concepts (intent/receipt/etc.) exist as schemas/payloads, never as base code; `bash scripts/verify-mvp` passes
  - verify: test -x scenarios/stint/test && bash scripts/verify-mvp
- [ ] VANTA-M-005: Scenario B end-to-end (deployment accountability, MVP_PLAN §7)
  - acceptance: `scenarios/deploy/` runs the full Scenario B sequence (source → build → test → deploy → third-party verification → originator gone) against the local test history, explicitly exercising: multiple attestors on the same content, attester ≠ performer, originator ≠ committer, the same artifact referenced by multiple actors, third-party recomputation by hash; `./scenarios/deploy/test` (executable, timeout-capped) passes including the VANTA-M-003 verifier over the resulting history; `bash scripts/verify-mvp` passes
  - verify: test -x scenarios/deploy/test && bash scripts/verify-mvp
- [ ] VANTA-M-006: Originator independence + interpretation freedom
  - acceptance: `scenarios/independence/` demonstrates BOTH: (a) originator-independence — after the scenario originator's process/state is stopped or deleted, the VANTA-M-003 verifier still validates the full history and reconstructs derivation chains from public data alone; (b) interpretation freedom — two independent interpretation programs (e.g. an audit-log projection and a provenance summary) each compute a different, correctly derived interpretation from the same history, with neither interpretation stored by the base; `./scenarios/independence/test` (executable, timeout-capped) passes; `bash scripts/verify-mvp` passes
  - verify: test -x scenarios/independence/test && bash scripts/verify-mvp
- [ ] VANTA-M-007: MVP report and success-criteria audit
  - acceptance: all VANTA-M-001..006 evidence reviewed; the 5-question change gate applied to every open gap in `deep-work/findings.md`; `deep-work/mvp-report.md` written (verdict line `MVP PASS`, `MVP INCOMPLETE`, or `MVP NOT READY`; a table mapping each MVP_PLAN §11 sub-criterion to its evidence; the substrate-boundary list; the findings list with classifications; any NEEDS_HUMAN items; recommended next step = S1); create the marker file `deep-work/state/MVP_STRICT` (flips the verifier to strict); `bash scripts/verify-mvp` passes in strict mode
  - verify: test -f deep-work/state/MVP_STRICT && test -s deep-work/mvp-report.md && bash scripts/verify-mvp
- [ ] VANTA-M-008: (continuation) Hardening — test depth and failure cases
  - acceptance: extend the test suites in `base/`, `base/verifier/`, and `scenarios/` with additional adversarial/failure cases (truncated records, cross-schema confusion, replayed/duplicate records, broken rotation chain) — every added case must be a genuine acceptance test with a named expectation; all entrypoints still pass under their timeouts; `bash scripts/verify-mvp` passes
  - verify: bash scripts/verify-mvp
- [ ] VANTA-M-009: (continuation) Documentation pass
  - acceptance: `base/README.md` documents the reference implementation (layout, how to run tests, the substrate-boundary interface, how the verifier is kept independent) and `deep-work/VERIFICATION.md` is updated with the new `verify-mvp` contract and the `base/` + `scenarios/` layout; no behavior changes; `bash scripts/verify-mvp` passes
  - verify: test -s base/README.md && bash scripts/verify-mvp
- [ ] VANTA-M-010: (continuation) Review and simplify previous work
  - acceptance: review this run's `base/` and `scenarios/` code; remove dead code, duplicate helpers, and over-generalization; keep the CP1 interop property intact (re-run the affected test entrypoints after each change); record what was simplified and why in `deep-work/findings.md`; `bash scripts/verify-mvp` passes
  - verify: bash scripts/verify-mvp

## Notes for human reviewers (ignored by the Stint parser; not in worker prompts)
- Horizontal-work follow-on: this mission intentionally does **not** implement Vanta Work,
  Cosmos/IBC, Akash or Lava. After the base envelope is stable, use
  `deep-work/HORIZONTAL_WORK_MISSION.md` to falsify that above-base hypothesis without changing
  the current MVP ontology.
- Mission shape: VANTA-M-001..007 are primary (build); VANTA-M-008..010 are
  continuation tasks — the coordinator reaches them only if the primary work
  completes before the session deadline, so an early-finished run spends its
  remaining budget on hardening, docs, and self-review instead of stopping.
- Ordering: M-001 → M-002 → M-003 (verifier is independent of the reference
  impl) → M-004/M-005 (need M-002+M-003; they degrade to spec-only runs if
  either parked, and the M-007 report must say so honestly) → M-006 → M-007.
  If M-002 or M-003 parks after its attempt cap, the honest verdict in
  M-007 is "MVP reference implementation incomplete: <gap>".
- Substrate deferral: this run deliberately stops at the substrate boundary
  (local test history). MVP_PLAN §10 places substrate choice (S1) at CP2,
  after CP1 evidence + author sign-off — this mission must not pick a
  production substrate.
- `scripts/verify-mvp` ships with the baseline tree (this run's verifier,
  authored by the operator): LENIENT mode validates whatever exists and passes
  on the pristine tree, so no task false-fails on a later task's missing
  artifacts — every per-task verify ends in it, exactly like `verify-cp1` did
  for CP1. VANTA-M-007 creates `deep-work/state/MVP_STRICT`, which flips the
  verifier to STRICT for its own final check (full artifact set + verdict line
  required). Each test entrypoint self-caps at 120 s per the mission
  contract; the verifier runs them with a 100 s cap so the mission-level
  check stays under the coordinator's 3-minute verification cap.
- Execution host (from the P0 box probe): Ubuntu 24.04, Node v22 + Python 3.12
  with `cryptography` present, no Go toolchain (Go only via prebuilt static
  binary — prefer Node or Python for this run). The worker's shell policy is
  deny-by-default; ordinary commands (git, bash, node, python3, timeout,
  cat/ls/grep, mkdir) run freely.
