# Pilot Design — Agentic-Serving Characterization

*Purpose: the document to screen-share at the Vinita sync. It maps to the agreed agenda —
pilot design, instrumentation/analysis ownership, and (implicitly) what work belongs to
whom for the byline conversation.*

**Operative target:** MLSys 2027 Industry Track (~Oct 2026). Measurement-and-characterization
paper, public benchmarks + open infra only. Not a system, not a recipe, not a kernel paper.

**Lead contribution (C1):** a rigorous, open-infra quantification of the *realized-vs-available
cache-locality gap* under realistic agentic + mixed traffic, expressed as
**cost-per-verified-iteration** curves — plus, as a cross-cutting artifact (C3), a released
**mixed chat×agent, cost-labeled, OTel-format trace + harness**, since no public *mixed chat×agent,
cost-labeled, open-infra* serving trace exists (as of a dated search; the broader "first public
agentic trace" headline is already eroded — see `04-ideas/graveyard.md`).

> Framing discipline (from the SOTA pass): the *mechanism* space (eviction/TTL/sharing/scheduling)
> is now crowded — Continuum/CacheTTL, KVFlow, KVCOMM, Sutradhara, Helium, SparseX, TokenDance.
> The naive "agentic ≠ chat" characterization is table stakes. Our defensibility is the
> *combination*: rigor + breadth + open reproducibility + the trace artifact + precise framing.
> Each individual measurement below is adjacent to published work; the bundle is not.

---

## Hypotheses (falsifiable, each with a kill criterion)

**H1 — The locality gap is real on open infra, and interleaving is a distinct driver.**
When chat and agent traffic share one vLLM/SGLang instance under a bounded KV budget, the
*realized* prefix-cache hit rate for agent requests falls well below the *available* reuse
measured in isolation (the high-reuse regime in 2605.26297 — record the exact figure + denominator
in `02-literature/sota-verified-2026.md` before quoting a precise range), and a measurable share of the
drop is attributable to **eviction pressure from interleaving**, separable from intra-agent
context churn.
- *Why non-obvious:* 2605.26297 reports high reuse; Sutradhara reports collapse — but Sutradhara
  is synthetic-at-scale and attributes collapse to churn + eviction *within* agentic requests.
  Nobody has cleanly isolated the multi-tenant-interleaving contribution on open infra.
- *Test:* run ReAct on τ²-bench isolated vs mixed_0.50; compare available reuse (offline,
  infinite cache) to realized hit rate (online, bounded); attribute the gap via cache-event logs.
- **KILL:** if isolated realized hit rate already collapses (no headroom for tenancy to matter),
  the story is churn, not interleaving — and churn is already a mechanism-paper topic. Pivot.

**H2 — Cost-per-verified-iteration grows super-linearly with horizon, and the curve is
cache-policy-sensitive ("the Cost of Grit").**
Serving cost per *verified* iteration rises faster than linearly as horizon grows under bounded
cache, and the inflection shifts with retention policy — a structure $/token hides.
- *Why non-obvious:* capability-side work (More with Less; framework cost studies) measures
  $/patch but not the serving-knob sensitivity on open infra.
- *Test:* sweep max-iters {8,16,32} under {none, lru, retain_during_tool}; plot cost-per-verified-
  iteration tied to task success.
- **KILL:** if the curve is linear and policy-insensitive, there is no "tax" story.

**H3 — Tool-gap timing has exploitable phase structure that static eviction gets wrong.**
GPU-idle is dominated by tool-call gaps whose timing follows the read/explore→execute/write phase
(2605.26297); static LRU therefore evicts caches systematically at the wrong moments, and a
phase-aware retention window would recover realized-hit-rate loss (shown in *simulation*, not built).
- *Why non-obvious:* the phase structure is known; its quantified implication for retention error
  under realistic load is not. This is measurement that *motivates* a mechanism without building one.
- *Test:* measure tool-gap distribution + GPU idle by cause across the trajectory; offline-simulate
  realized hit rate under LRU vs phase-aware retention.
- **KILL:** if tool-gap timing is effectively random, or GPU idle is dominated by scheduling/batching
  rather than tool gaps, reframe.

**H4 — A public mixed/agentic trace + harness reproduces H1–H2 (artifact-as-contribution).**
A small, cost-labeled, OTel-format trace of mixed chat×agent traffic on open infra is sufficient
for others to replay and reproduce the gap and the cost curve.
- *Why it matters:* ServeGen released a *generator* on real but *non-agentic* data; no public
  *agentic/mixed* serving trace exists. Differentiation = tenancy-mix + cost labels + open infra.
- **KILL:** a comparable mixed/agentic trace ships first (watch Continuum repo, lmcache, ServeGen
  extensions). C3 survives only in this narrowed tenancy-mix + cost-labeled form.

---

## The pilot cell (run first — de-risks everything)

ReAct × τ²-bench × {isolated, mixed_0.50} × {lru, retain_during_tool} × 50 scenarios × 3 repeats
= 600 trajectories on one vLLM config. ~1 week, likely <$300 of rented H100 time.
Primary readouts: available vs realized hit rate; cost-per-verified-iteration; tool-gap distribution.
(Config in `experiments/matrix.yaml`; metric contract in `harness/trace_schema.py`.)

---

## Metric definitions (the contract)

- **available reuse** — reusable input tokens under an *infinite* cache, computed offline by replay.
- **realized hit rate** — prefix-cache hit tokens under the *bounded* online cache (engine counter).
- **locality gap** — available − realized, in [0,1]. The core C1/B quantity.
- **cost-per-verified-iteration** — total $ (or GPU-seconds) / iteration, *only for tasks that pass
  verification* (FAIL_TO_PASS or τ²-defined success). Null for failures.
- **tool-gap** — wall-clock GPU idle between tool dispatch and return.

---

## Proposed ownership split (strawman for the sync)

| Layer | Owner | Scope |
|---|---|---|
| Serving-internal instrumentation | **Vinita** | vLLM/SGLang engine config, prefix-cache + eviction counters, bounded-KV setup, mixed-traffic load generation, GPU-busy/queue timing |
| Workload + benchmark harness | **Minseok** | running ReAct on τ²-bench/SWE-bench, chat-trace interleaving, scenario management |
| Offline analysis | **Minseok** | infinite-cache replay → available reuse, cost-per-verified-iteration, phase labeling, stats |
| Trace schema / OTel spans | **shared** | `trace_schema.py` is the seam — co-own it |
| Framing, lit, writing | **Minseok** (lead) | — |

The instrumentation layer is the credibility-critical part and is squarely Vinita's. That is the
honest basis for the author-order conversation — decide a *proposed* order before the meeting.

---

## Open questions to resolve at the sync

1. **Alignment first:** does Vinita agree C1 (measurement) is the lead, not a recipe/optimization
   paper? Everything below is premature if not.
2. **Bandwidth:** realistic hrs/week each. (~10 hrs/wk × ~5–6 wks per person is the binding constraint.)
3. **Compute funding:** Stanford credits / NVIDIA credits / personal?
4. **Author order:** given the instrumentation weighting, what ordering are we proposing?
5. **What I have NOT pre-built:** the engine instrumentation, on purpose — it's a co-design item.

---

## Open design issues to resolve at the sync (from 2026-06-13 adversarial review)

Settle these **before** spending GPU budget — they affect whether H1–H3 are even identifiable:

1. **`locality_gap` definition + bounds.** The contract above says `available − realized` on a common
   denominator; the code (`trace_schema.py`) normalizes by reusable tokens and can return values
   outside [0,1] (it returns −0.4 for realized>reusable). Pick ONE definition (recommend: both rates
   over *total eligible input tokens*), make code + docstring match, and validate `0 ≤ realized ≤ available ≤ 1`.
2. **Trace schema can't yet compute available reuse or attribute eviction.** It records token *counts*
   but not prompt token-IDs / block hashes, global request ordering + timestamps, tokenizer revision,
   cache keys, eviction victims, or tenant provenance — so the infinite-cache replay (and "did chat
   evict agent blocks?") is not computable. Add these (Vinita owns the serving-internal fields). Same
   gap makes the "OTel-format" label aspirational: add real trace/span/parent IDs + timestamps or drop the claim.
3. **Tenancy vs offered-load confound.** `isolated` vs `mixed_0.50` changes *composition* AND total
   load/concurrency at once. Hold the agent trajectories fixed and add chat as a *rate-matched*
   background (control total token-arrival rate + concurrency) so the gap is attributable to interleaving.
4. **Bounded-KV budget is unset** (`bounded_cache_blocks=-1`; no matrix axis). Add a positive
   block/byte budget as a first-class axis; ideally sweep ≥2 pressure regimes.
5. **Cost-per-verified-iteration has horizon-dependent survivor bias** — nulling cost on failures drops
   the expensive long-horizon failures, exactly where "Cost of Grit" lives. Report cost-per-verified-*task*
   including failed-attempt cost + a success/censoring curve, over all attempts (not just successes).
6. **"Tool-gap" ≠ GPU-idle.** `tool_gap_ms` is tool wall-time; under mixed tenancy the GPU serves other
   requests during it. H3 needs an engine-wide utilization timeline to compute idle-by-cause.
7. **Executor/aggregation don't match the design.** `run_pilot.main` loops only tenancy×policy (drops
   repeats + horizon → 4 cells, not 600); `aggregate` returns one global mean, not grouped/paired
   estimates with CIs. Fix the cell runner + grouped, token-weighted, paired stats.

*(Source: adversarial review, 2026-06-13. Items 1 & 4 were also flagged in the internal pass.)*
