# Vanta — Decisions and Hypotheses (with reasoning)

Format: current position → evidence for → counter-evidence → alternatives → confidence →
what would cause a revisit.

D1. **Blockchain is intrinsic to Vanta.** — *Held, sharpened (2026-02-09).*
Position: Vanta requires decentralized consensus + staking because its core is the
*enforcement* of commitments between mutually distrustful parties (shared value state +
canonicity without an authority + economic security on maintainers), not mere recording.
For: the architecture ladder (VISION §2) — every simpler system stops at recording/detection
and needs a trusted party to resolve; the machine-actor use case excludes pre-vetted
federations.
Against: a bonded federation might be "good enough" for a closed set; many real users would
accept a trusted operator (which is why most commerce runs on DBs).
Alternatives: transparency log (recording only); consortium chain (permissioned ordering).
Confidence: high that *some* decentralized consensus is required; moderate that it must be
*permissionless*.
Revisit if: Vanta's value proves purely informational (no value movement), or a bonded
federation demonstrably covers the target use cases.

D2. **Vanta stores evidence/history, not interpretations.**
Position: protocol stores thin facts (commitments, receipts-as-evidence-commitments,
settlements, disputes); reputation/prices/quality are computed by apps over the public
history.
For: avoids an arbitrary, gameable, politically charged universal score; cross-domain
portability; matches "owns the evidence, apps own the interpretation."
Against: some apps may want a protocol-level score (simpler DX); event-sourcing everything
adds complexity.
Alternatives: protocol-level base score (rejected so far); no reputation data at all (too
thin).
Confidence: high.
Revisit if: two independent apps cannot extract useful, stable interpretations from the same
history (evidence too thin).

D3. **The ledger primitive is one typed, signed, hash-linked "fact"; the protocol defines a
base family (intent, commitment, receipt, settlement, dispute).**
Position: single substrate primitive + governed base family of kinds; apps extend via schema
governance.
For: clean Cosmos-Msg-like data model; the family maps 1:1 to the lifecycle and to Stint;
verification-agnostic evidence keeps it cross-domain.
Against: one primitive may be over-abstract (five families with own semantics might be
clearer to developers); "fact" is a vague word.
Alternatives: family-of-five primitives (B); "commitment" as single primitive (C, rejected —
evidence isn't a promise); capability (D, kept only for the identity layer).
Confidence: moderate.
Revisit after: writing out all base fact kinds with fields + validation rules (next concrete
step).

D4. **Vanta is a general protocol, not a compute marketplace. Stint is the first app, not
the whole story.**
Position: Vanta-level = fact kinds, escrow/stake state machine, consensus, identity, dispute
rules, history. Stint-level = compute-specific evidence schemes, provider software, market
dynamics.
For: cross-domain tests (API, storage, exchange) survive without forking record types; the
differentiation vs. Akash is shared history + first-class evidence.
Against: if all real usage is compute, generality is speculative weight.
Confidence: moderate-to-high (pattern tests passed, small sample).
Revisit if: the first two real apps are both compute markets.

D5. **The economic layer is a separate concern from the record layer; a native asset (if any)
serves protocol security (staking/slashing/fees), while services are priced in stablecoins or
other assets.**
Position: research the *functions* the protocol needs (security, spam control, escrow
collateral) before any token design; a token is architecturally meaningful only if it backs
slashing.
For: stablecoins can't be slashed (IOUs); Bittensor and Cosmos both separate a security asset
from service pricing.
Against: two assets complicate onboarding; Vanta might reuse an existing security asset.
Confidence: low-to-moderate (deliberately parked — a guardrail against speculative
tokenomics, not a decision yet).
Revisit when: the dispute/slashing design (Q2) is concrete enough to name what must be
stakeable.

D6. **Vanta is verification-agnostic: receipts commit to evidence under a declared scheme
(self-attestation → two-party → bonded verifier → ZK proof); the protocol checks scheme
conformance, not ground truth.**
For: cross-domain generality (compute/storage/APIs have different evidence schemes);
optimistic-to-ZK progression without protocol forks; matches the "needs to verify, doesn't
need to know" principle.
Against: L0/L1 evidence is gameable — the system's real security depends on two-sided staking
+ dispute fallback (Q2); accepting weak evidence by default may be unsafe by default.
Confidence: moderate.
Revisit after: the base evidence-scheme registry and dispute fallback are designed.

D7. **Re-centering: the base MVP is V1 (typed shared history); the economic layer (V2) is a
branch above the base.** (2026-02-09, plan phase.)
Position: base MVP = immutable typed-history protocol; V3 (receipts/accountability) reveals
base properties (portable evidence, provenance, continuity, reconstruction); V4 (state layer)
is a compatible branch used only to pressure-test; V2 (escrow/staking/settlement/tokens/
machine commerce) sits above the base and is not a base requirement.
For: the author's explicit constraint (original vision is the constraint); the original
starting points (typed records → shared history, portability, multi-app interpretation) are
all V1/V3; the economic framing entered through the Stint thread.
Against: v0.1 research found enforcement to be the strongest "why blockchain" argument; a
recording-only base could look "weaker" (a transparency log can also record). Rebuttal: the
base's blockchain requirement is canonicity without an operator + permissionless
contribution + liveness (I5/I6), which logs/federations do not provide; enforcement is a
branch requirement, not a base one.
Alternatives: keep the economic center of gravity (v0.1 lean) — rejected per constraint;
transparency-log-only base (no blockchain) — rejected per foundational assumption 2.
Confidence: high (author-directed re-centering, recorded for continuity, not a research
conclusion).
Revisit if: a spike shows no existing substrate can meet I5/I9 without forcing
security/economic machinery into the base, or the CP3 demo shows the recording base is
unusable for all intended consumers (a signal consumers actually need enforcement — V2).

## Change log
- 2026-02-09 — initial v0.1. Vision reconstructed; "why blockchain" sharpened from
  "immutability" to "enforcement without an authority" (recording vs. enforcing; canonicity
  as a computable property; economic security on maintainers); cross-domain tests of the
  commitment/receipt/settle pattern (API, storage, exchange); on/off-chain boundary working
  rule; base-primitive hypothesis (typed fact + base family); competing versions V1–V4 kept
  alive with a lean toward "enforced commitment as the center of gravity."
- 2026-02-09 (plan phase, continued) — v0.2 base plan (MVP_PLAN.md) supersedes the v0.1
  base plan found in the repo (archived: research/archive/MVP_PLAN_v0.1.md). The v0.1 plan
  baked the economic (V2) layer into the base: enforcement-core invariant, escrow/stake/fee
  state, evidence-scheme registry, intent/commitment/receipt/settlement/dispute/transfer
  fact family, test security asset, Cosmos SDK app-chain as leading candidate. v0.2 removes
  all of these from the base per the author's constraint (original vision is the constraint);
  full diff table in MVP_PLAN.md §1.5.