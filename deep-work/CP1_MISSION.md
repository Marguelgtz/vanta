# Vanta CP1 — S0/S3/S4 evidence before substrate selection

## Objective

Produce the evidence that moves Vanta from CP0 to CP1. The governing living plan is
`research/MVP_PLAN.md` — read it first (especially §2 invariants I1–I9, §3 facts vs
attestations, §4 primitives, §7 scenarios, §9 spikes S0/S3/S4, §10 change gate), then read
`deep-work/VERIFICATION.md` (artifact layout and verification contract).

This run completes:
- S0 — canonicalization & identity: one unambiguous canonical record representation, proven
  by two genuinely independent implementations over shared fixtures;
- S3 — full paper-walk of both pressure-test scenarios (MVP_PLAN §7) written as concrete
  Vanta record sequences;
- S4 — key rotation as a record-level convention, only as small as it needs to be.

You are producing checkpoint evidence, not building Vanta. No substrate choice (S1), no
base build, no economics. The original Vanta vision and invariants I1–I9 are the rigid
constraint; the implementation path is living.

First actions in every invocation: re-read the current task's acceptance; check `git
status` and the artifacts listed in `deep-work/VERIFICATION.md`; resume rather than restart.
When evidence challenges the base: record a finding in `deep-work/findings.md`, run the
5-question change gate (MVP_PLAN §10), mark base-affecting findings `NEEDS_HUMAN`, and
continue independent safe work.

## Success
- The record envelope (MVP_PLAN §4) has one unambiguous canonical representation; exactly which bytes are hashed, which bytes are signed, and how the record identity is derived is documented (s0/envelope.md) and implemented
- Two independent implementations (different languages, no shared code or libraries) produce byte-identical canonical bytes and record IDs for the shared fixtures, and each verifies the other's Ed25519 signatures (evidence in s0/interop.md, re-runnable through each implementation's test entrypoint)
- Equivalent logical records (field-order/encoding variants) produce identical canonical bytes, and `references[]`/`commitments[]` treatment is deterministic and test-proven in both implementations
- The complete Scenario A (Stint-shaped, §7) is a concrete record sequence; every step is classified as base (Actor/Schema/Record/History) or above-base; an explicit check shows no Stint-only primitive had to enter the base
- The complete Scenario B (deployment/software accountability, §7) is a concrete record sequence exercising: multiple attestors on the same content, attester ≠ performer, originator ≠ committer, the same artifact referenced by multiple actors, third-party recomputation by hash, and verification after the originator is gone
- Every capability gap that would require a new base primitive is recorded in deep-work/findings.md with the 5-question gate applied; base-level changes are marked NEEDS_HUMAN, never applied
- Key rotation (S4) is demonstrated as a record-level convention without new protocol machinery — or its impossibility is argued precisely with reasons
- deep-work/cp1-report.md exists with an evidence-backed verdict (READY FOR CP1 / READY WITH FINDINGS / NOT READY) mapping every Success criterion to its evidence
- `bash scripts/verify-cp1` passes; in the final task it must pass in strict mode (marker deep-work/state/CP1_STRICT)

## Constraints
- Rigid for this run: invariants I1–I9, the facts/attestations split (protocol knowledge vs attested claims), and the primitive set Actor/Schema/Record/History (MVP_PLAN §2–4). Never modify these silently.
- If evidence challenges an invariant or primitive: record the finding, run the 5-question change gate, classify it, mark it NEEDS_HUMAN if it affects the base, and continue safe work. You do not resolve base-level questions.
- Permissionless contribution is a hard base requirement for this run (frozen as A8). Do not redesign it; if its feasibility is seriously challenged, record that for human review.
- Substrate-neutral: no EVM/Solana/Celestia/Cosmos/custom-L1 choice, prototype, or dependency in this run. S0 code is pure local computation (canonicalization, hashing, signing).
- No economics in the base: no token, escrow, stake, slashing, settlement, fees, or value transfer in any base artifact. Economic steps may be *described* in the Stint scenario strictly as above-base.
- No Stint ontology as Vanta vocabulary: intent/commitment/receipt/settlement/dispute/provider/consumer/verifier/reputation are Stint *schemas* inside scenario documents — never Vanta primitives.
- Out of scope: S1, substrate selection, the full base build, custom consensus, generic databases/app-state platforms, reputation systems, privacy/ZK, availability guarantees.
- Keep protocol knowledge (signature, inclusion, typing, references, commitments) strictly separate from attested claims in every artifact. Never promote an external-world claim to protocol truth.
- Reversible ordinary choices (language pair from the shortlist, fixture shapes, file layout, naming, test organization, library choice) are yours to make; record each as a finding in deep-work/findings.md. Ontology-defining or production-defining choices are findings + change gate, never silent decisions.
- Each implementation stays small and self-contained (target ≤ ~300 lines including tests; standard library or one well-known pure crypto/serialization library). No frameworks, no shared library between the two implementations.
- Do not modify existing research/ documents; new artifacts go in the layout defined in deep-work/VERIFICATION.md.
- The coordinator verifies each task with that task's own `verify:` command: a check of the task's own artifacts, ending in the lenient `bash scripts/verify-cp1` (VANTA-007's runs strict, after it creates the marker). A task is VERIFIED only when its own verify command passes — the lenient cumulative verifier alone passes on an empty worktree and is never sufficient by itself.

## Verification
bash scripts/verify-cp1

## Tasks
- [ ] VANTA-001: Design the S0 canonical envelope spec and the shared fixtures
  - acceptance: s0/envelope.md fully specifies the canonical form (field order and encodings; exactly which bytes are hashed for the record ID; exactly which bytes are signed; how references[] and commitments[] are normalized; how schema_id binds the payload; and the statement that the author (signer) is the only protocol-level identity — originator/performer/attester are schema-level payload concepts) and s0/fixtures/records.json holds >= 7 language-neutral logical records (a minimal record; multi-reference; multi-commitment; unicode + empty fields; a nested payload; a record that references an earlier fixture by alias; an attestation signed by author A whose schema-level originator/performer field names a *different* actor O — O ≠ committer, referencing an earlier fixture); deep-work/findings.md records the chosen language pair from the shortlist (Node.js v22 / Python 3.12 / Go — probe the toolchains of the environment where the work runs and include evidence that both work for Ed25519 there; Go needs no toolchain in that environment if it ships as a prebuilt static binary) plus a reversibility note; `bash scripts/verify-cp1` passes
  - verify: test -s s0/envelope.md && test -s deep-work/findings.md && test -s s0/fixtures/records.json && bash scripts/verify-cp1
- [ ] VANTA-002: First independent implementation (expA)
  - acceptance: s0/expA/ implements the envelope (canonicalization, record ID, Ed25519 sign/verify) in the first chosen language, self-contained; its test suite covers determinism, equivalent-logical-records, references/commitments normalization, and sign/verify round-trip, and runs via ./s0/expA/test; fixture outputs (per fixture: canonical hex, record ID, signature, public key) written to s0/expA/out/records.json in the shape from deep-work/VERIFICATION.md; `bash scripts/verify-cp1` passes
  - verify: test -x s0/expA/test && test -s s0/expA/out/records.json && bash scripts/verify-cp1
- [ ] VANTA-003: Second independent implementation (expB) plus cross-language interop
  - acceptance: s0/expB/ independently implements the same spec in the second chosen language (no code copied from expA; no shared library); ./s0/expB/test passes and includes the interop check: byte-identical canonical bytes and record IDs for every shared fixture, A's signatures verify under B, and B's under A (A's out/records.json consumed as input); s0/interop.md records the results; `bash scripts/verify-cp1` passes
  - verify: test -x s0/expB/test && test -s s0/expB/out/records.json && test -s s0/interop.md && bash scripts/verify-cp1
- [ ] VANTA-004: Scenario A paper-walk (Stint-shaped, MVP_PLAN §7)
  - acceptance: s3/scenario-stint.md (with machine-checkable s3/scenario-stint.json) expresses the full Scenario A sequence (intent → offer → off-chain work → evidence commitments → receipt → reputation interpretation) as concrete records with canonical bytes/IDs from expA where available; every step classified as base primitive / schema or domain concept / off-chain evidence / interpretation / excluded above-base behavior; includes the explicit check that no Stint-only primitive had to enter the base; gaps logged in deep-work/findings.md; `bash scripts/verify-cp1` passes
  - verify: test -s s3/scenario-stint.md && test -s s3/scenario-stint.json && bash scripts/verify-cp1
- [ ] VANTA-005: Scenario B paper-walk (deployment / software accountability, MVP_PLAN §7)
  - acceptance: s3/scenario-deploy.md (with s3/scenario-deploy.json) expresses the full Scenario B sequence (source → build → test → deploy → third-party verification → originator gone) as concrete records; explicitly exercises and evidences: multiple attestors on the same artifact content, attester ≠ performer, originator ≠ committer (records about O committed by others, with O committing nothing of its own in at least one step), the same artifact referenced by multiple actors, third-party recomputation by hash, and verification after the originator's services are gone; classification table as in VANTA-004; gaps logged in deep-work/findings.md; `bash scripts/verify-cp1` passes
  - verify: test -s s3/scenario-deploy.md && test -s s3/scenario-deploy.json && bash scripts/verify-cp1
- [ ] VANTA-006: S4 — key rotation as a record-level convention
  - acceptance: s4/rotation.md specifies the minimal convention (a rotation as a typed record; attribution follows rotation chains) and either demonstrates it with concrete records (optionally reusing expA) or argues precisely why continuity cannot be reconstructed without new protocol machinery; states the conclusion (expected: no protocol machinery needed) and whether it cost any; findings logged; `bash scripts/verify-cp1` passes
  - verify: test -s s4/rotation.md && bash scripts/verify-cp1
- [ ] VANTA-007: CP1 challenge and report
  - acceptance: all evidence from VANTA-001..006 reviewed; the 5-question change gate applied to every open gap in deep-work/findings.md; deep-work/cp1-report.md written (verdict READY FOR CP1 / READY WITH FINDINGS / NOT READY; a table mapping each Success criterion to its evidence; the findings list with classifications; any NEEDS_HUMAN items; recommended next step = S1); create the marker file deep-work/state/CP1_STRICT; `bash scripts/verify-cp1` passes in strict mode
  - verify: test -f deep-work/state/CP1_STRICT && test -s deep-work/cp1-report.md && bash scripts/verify-cp1

## Notes for human reviewers (ignored by the Stint parser; not in worker prompts)
- The Stint Deep Work parser folds into every reconstructed worker prompt: Objective lines,
  Success bullets, Constraints bullets, and each task's objective + acceptance line. This
  section and any other unknown section is ignored by the coordinator and exists for humans.
- Verification is cumulative by design: `scripts/verify-cp1` validates whatever exists
  (lenient mode), so no task can false-fail on a later task's missing artifacts — the
  live-run lesson from Stint's DEEP_WORK.md §8. It becomes strict only after VANTA-007
  creates `deep-work/state/CP1_STRICT`. Each implementation's test run is capped at 80 s
  so the mission-level command stays inside Stint's 3-minute verification cap.
- Task order: 001 → 002 → 003 (interop needs both implementations); 004/005 need only 001
  and degrade gracefully (aliases instead of canonical bytes) if 002/003 are still pending;
  006 needs 001; 007 is last. If 002 parks after its attempt cap, 003 will also park;
  004/005/006/007 remain executable and the CP1 verdict can still be honest
  (READY WITH FINDINGS or NOT READY, with the interop gap named).
- Per-task `verify:` commands (table in `deep-work/VERIFICATION.md`): the Stint coordinator runs a
  task's own verify command after each attempt and falls back to the mission-level command only when
  a task defines none. Because the lenient cumulative verifier passes on an empty worktree (by design),
  every task carries a scoped command so VERIFIED means "this task's evidence exists and is valid",
  not "the cumulative script happened to exit 0".
- Execution target (P0 box probe, 2026-09-03; the first run executes on a rented GPU box over SSH
  with the worker = headless Hermes on the box): Ubuntu 24.04, Node v22.23.2, Python 3.12 +
  cryptography, git, no Go toolchain (a prebuilt static Go binary runs without one), model
  `qwen3.8-27b` at `http://127.0.0.1:8080/v1` on the box. The worker's shell policy is
  deny-by-default: ordinary commands (the ones this mission uses — git, bash, node, python3, timeout,
  cat/ls/grep) run freely; dangerous commands are denied in unattended one-shot runs; hardline
  commands (wipe/reboot class) are always blocked; file edits are unrestricted within the worktree.
  Provisioning and policy detail: Stint `docs/DEEP_WORK_GPU_HERMES_PLAN.md`.