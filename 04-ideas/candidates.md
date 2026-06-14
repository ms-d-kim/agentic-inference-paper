# Candidate Ideas

*Carried from the 2026-06-10 working session; verification status updated 2026-06-13.
Exploration mode: candidates stay live until a pilot collapses the choice. Every candidate has a
kill criterion; killed ideas move to `graveyard.md`. Check the graveyard before proposing anything
"new."*

## C1 — Iteration-cost curve ("The Cost of Grit") — **LEAD**
- **Claim:** measure cost/latency per *verified* iteration vs horizon × cache policy × compaction
  policy × tenancy × model size, on vLLM/SGLang + public benchmarks; quantify the locality tax.
- **Impact:** the missing meter; serving teams and agent builders both act on it.
- **Collisions:** adversarially checked 06-10. Distinguish from: Don't Break the Cache (2601.06007 ✓,
  provider-API level only), the Efficiency-Frontier-style analytical models (e.g. 2605.23929 ✓),
  More with Less (2510.16786 ✓, capability side). "SideQuest" and "Agent Memory" collisions are
  ⚠ UNVERIFIED — see `02-literature/sota-verified-2026.md`.
- **Status:** pilot pending. See `05-experiments/pilot/`.

## C2 — Cache-aware context-edit policy formalization
- **Claim:** treat context edits as decisions with cache-write/recompute costs + quality risk;
  policy search; quality×cost frontier across agents and cache regimes (incl. CacheBlend-class).
- **Status:** watching; natural sequel or pivot of C1. Home venue: COLM 2027.

## C3 — Mixed-tenancy, cost-labeled public trace + harness
- **Claim:** release the chat×agent interleaved serving trace with arrival dynamics, cache events,
  cost labels, OTel-format cross-layer spans + the collection harness.
- **Collisions:** trace-alone eroded (Continuum 2511.02230 ✓; "lmcache-agent-trace" ⚠ unverified).
  **Tenancy-mix + cost labels on open infra is the surviving differentiation.** Note ServeGen
  (2505.09999 ✓) released a generator on real but non-agentic data.
- **Status:** bundled into C1's instrumentation by design. De-risked home: NeurIPS D&B.

## C4 — Runtime↔engine hint interface (value-of-hints study → spec)
- **Claim:** measure marginal value of each hint type (resume-time, fan-out, durable-prefix markers)
  vs inference-only baselines, then propose the minimal spec.
- **Status:** parked behind C1 (C1 produces the value measurements).

## C5 — Iteration-economics metering (product-shaped)
- **Claim:** cost-per-verified-iteration and realized-vs-available locality as first-class serving
  metrics/SLOs; reference implementation on open infra.
- **Status:** the PM-role twin of C1. **Build internally at NVIDIA if at all — keep OUT of this repo**
  (IP separation). Design notes only.

## C6 — Harness-conditional benchmarking methodology
- **Claim:** quantify harness/model attribution (home-field advantage) and cost-per-success norms.
- **Status:** low-cost background option; could be a workshop paper.
