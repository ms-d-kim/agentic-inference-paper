# Observability & statistical power — how the two blockers actually get solved

*Makes the two BLOCKER pilot issues concrete: #15 (can we even see the cache per request?), #2/#11
(can we recompute the ideal?), #14 (is the denominator big enough?), #7 (is the effect bigger than the
noise?). If the answers here hold, the study is measurable AND a real contribution. If they don't, we
learn that for ~1 day of spike work instead of ~$600 of GPU.*

## 1. The instrumentation question — can we see the cache? (issue #15)

**What we need:** per-request **realized** reuse (the numerator) + per-tenant **eviction attribution**
("did chat evict *this* agent's blocks") — on open engines, ideally with no patch.

**What's exposed off-the-shelf, mid-2026:**
- **vLLM** ships `vllm:prefix_cache_queries` and `vllm:prefix_cache_hits` Prometheus counters
  (token-level: *queries* = prompt tokens seen, *hits* = tokens already cached), per-request
  `num_cached_tokens` in the response usage, eviction events via `SchedulerStats`, and `LLM.get_metrics()`.
  ([vLLM metrics docs](https://docs.vllm.ai/en/latest/design/metrics/), [counters issue](https://github.com/llm-d/llm-d-inference-sim/issues/356))
- **SGLang / RadixAttention** exposes a cache hit-rate metric.
- **LMCache** re-exposes cache metrics through the [vLLM `/metrics` endpoint](https://docs.lmcache.ai/production/observability/vllm_endpoint.html); Mooncake / llm-d add KV-pool stats.
- **Standardization is mid-flight, not done:** OTel genai semantic-conventions
  [issue #87](https://github.com/open-telemetry/semantic-conventions-genai/issues/87) proposes
  `gen_ai.server.kv_cache.{hit_rate, evictions_total, usage_ratio}` — not stable yet, so we can't assume it.

**Verdict:** the **numerator is gettable today** (per-request cached-token count, no patch). Aggregate
evictions are gettable. The one genuinely missing piece is **per-tenant eviction *attribution***.

**How we get attribution, in preference order:**
1. **Tag requests by tenant; read per-request `num_cached_tokens`.** Gives realized reuse per tenant with
   zero engine changes. (Do this regardless.)
2. **Block-owner lifecycle attribution — this is an engine *patch*, not "a few lines" (corrected
   2026-06-14 after Codex primary-source check).** vLLM's eviction telemetry exposes lifetime / idle-time /
   reuse-gap statistics — it does **not** carry the evicted block's id, owning request, or tenant. So
   "correlate `SchedulerStats` events to ownership" does **not** work off-the-shelf. Attribution requires a
   **version-pinned block-manager patch** that logs `(evicted_block_hash, owner_request_id, tenant)` at the
   moment of eviction, and that patch must be **validated against controlled known-eviction microbenchmarks**
   before it's trusted. Treat this as real instrumentation scope (Vinita's layer), and as a **C1 gate**:
   if the patch isn't feasible/validated, per-tenant victim attribution doesn't exist.
3. **Footprint-matched proxy (issue #3) — a weaker fallback, not equivalent.** Agent-only vs. agent+chat
   at a *matched* KV footprint gives a **delta** in realized reuse, but it does **not** name the victim
   block and cannot prove *chat* evicted *the agent's* state (the delta also moves with batch composition
   and scheduling). Report it as suggestive, not as causal attribution.

**First action — the instrumentation spike (1 day, 1 config, before any GPU spend):** confirm which of
1/2/3 the stock engines actually give us. This is the cheapest possible de-risk of issue #15.

### Wrong-layer tools: GPU profilers (Nsight) and reuse predictors (Tencent FlashMemory)

Two tempting shortcuts that **don't** source per-tenant eviction attribution, for the same root reason —
they live at the wrong abstraction layer:

- **Nsight Compute / Nsight Systems.** These are **kernel/hardware** profilers. They see SASS instructions,
  occupancy, warp stalls, and the **GPU's own L1/L2/DRAM** hierarchy — *not* the engine's PagedAttention
  block pool, which to the hardware is just undifferentiated HBM. A profiler cannot say "chat request #42
  evicted agent request #17's KV block," because "request," "tenant," and "KV block" don't exist at the
  layer it measures. Two further problems: Nsight **Compute** serializes kernel replay with heavy overhead —
  unusable on a live multi-tenant server; Nsight **Systems** (the timeline tool) can show the *consequence*
  of a miss (a prefill kernel firing again) **only if you NVTX-tag the work by request** — but that tag *is*
  the application-level fact you'd instrument in the block manager anyway, so the profiler adds overhead, not
  information. **Verdict:** profilers can *corroborate the cost* of eviction (recompute on the timeline);
  they cannot *attribute* it. Attribution is an engine/scheduler fact, captured at step 2 above.

- **Tencent's FlashMemory / Lookahead Sparse Attention** (`2606.09079`, project suspended). This predicts which
  KV chunks are *query-critical* for the **current** generation (a learned Neural Memory Indexer keeps ~13.5%).
  It is **intra-request attention sparsification** — a *mechanism* for deciding what *one* request can drop —
  not a *cross-tenant* observability tool, and not about who evicts whom under contention. Adopting a predictor
  would also flip us from a **measurement** paper to a **mechanism** paper, which we explicitly are not. The
  conceptual link is one-directional: reuse/criticality *prediction* is the kind of signal the *inferred*-contract
  systems (Continuum/CacheTTL, GoodServe) use to decide retention — so it belongs to the mechanism lineage we
  *measure the value of*, on the right-hand side of the seam, not to our instrumentation. We **observe** realized
  reuse and **replay** available reuse; we never need to **predict** it.

**Bottom line:** per-tenant eviction attribution is cheap and lives in exactly one place — the engine's block
manager (step 2). No profiler or predictor moves that needle; the 1-day spike confirms whether even the small
hook is needed.

## 2. The replay question — is it the *same* problem? (issue #2/#11)

**No — and it's the easier half.** The two are different axes:

| | online instrumentation (§1) | offline replay |
|---|---|---|
| computes | **realized** reuse (what actually got reused) | **available** reuse (the ideal, infinite cache) |
| depends on | the **engine** reporting its internals | **our harness** recording the request stream |
| hardest piece | per-tenant eviction attribution | nothing — it's our own log |

Replay = simulate an infinite cache over the **recorded ordered (request, prefix-block) stream** and count
how many blocks *could* have been reused. That needs only that `trace_schema` records, per request: the
token/block sequence (or block hashes) + arrival order + agent lineage. **All of that is in our control** —
it does not require seeing inside the engine.

So the uncertainty you flagged is real but **localized to §1**. Replay is gated by *what we choose to log*,
not by engine observability. The two overlap only at "log enough." And:

> **locality gap = available (replay) − realized (instrumentation).**

Concretely: even in the worst case where eviction attribution needs a patch (§1 step 2), replay still works,
because it never touches the engine. That's why replay is the tractable half.

## 3. Statistical soundness — enough to be a real contribution (issues #14, #7, #12)

Three independent things have to hold; each has a pre-registered guard:

- **Denominator floor (#14, BLOCKER).** The metric is cost-per-**verified**-task, so we need enough tasks the
  agent actually solves. A bare ReAct scaffold resolves maybe ~20–30% of SWE-bench Verified → at 50 tasks
  that's ~10–15 successes per cell, too few for a stable mean. **Fixes:** use a stronger published scaffold;
  pre-select a solvable subset; make τ²-bench (higher success rate) the *primary* curve and SWE-bench the
  *stress* arm; report successes-per-arm; widen N if the floor is too low. **Pre-register a minimum
  successes-per-cell** before spending.
- **Pre-registered MDE + power (#7) — NOT yet established (corrected 2026-06-14).** The 1,200-trajectory
  matrix is **not** "sized for 80% power" — there is currently **no variance estimate, no MDE calculation,
  and no power result**, and the effective sample is ~50 *tasks* (the 3 repeats share the same tasks), with
  arrival schedules and server runs adding a second cluster level. The honest order of operations: (1) run a
  micro-pilot; (2) estimate task-level and run-level variance (and intraclass correlation); (3) **then**
  pre-register a *cluster-aware* power calc (bootstrap/`delta-method` CI over **tasks**, not trajectories) +
  a minimum-successes-per-cell floor. Only after that can any "N is sufficient" claim be made.
- **Success-invariance measured, not assumed (#12).** Cost-per-task only compares across arms if the *set* of
  solved tasks is roughly stable. Greedy decode + fixed seeds, cache-on; the `none` arm is non-comparable by
  design; **measure** the drift, don't assume it away.

**Net:** the contribution is valuable iff *(numerator visible — §1)* AND *(denominator big enough — floor)*
AND *(effect bigger than noise — MDE)*. The spike (§1) plus a power calc on pilot data settle all three
**before** the full spend — which is exactly issue #19's "settle before you spend" gate, made concrete.
