# Reading Queue (priority order)

*Carried from 2026-06-10. ⚠ flags added 2026-06-13 — several references are UNVERIFIED; see
`sota-verified-2026.md` before citing or quoting figures.*

1. ⚠ **AutoLab** §4.3 harness ablation — verify the "+0.43" magnitude/conditions. UNVERIFIED paper;
   do NOT quote the figure until confirmed. (blocks quoting it)
2. **Agent Memory (2606.06448 ✓)** — REAL: *Characterization & System Implications of Stateful
   Long-Horizon Workloads* (Omri/Tambe, Stanford). HIGH — close characterization competitor; read for
   overlap with our characterization + cost-attribution angle. (The earlier ✗ / guessed 2603.04428 was wrong.)
3. ⚠ **SideQuest (2602.22603)** — UNVERIFIED; confirm it exists, then read eviction-policy details.
4. **Continuum / CacheTTL (2511.02230 ✓)** — repo README + any trace files; contents inventory.
5. **Don't Break the Cache (2601.06007 ✓, Lumer/PwC)** — methods section; reusable cache-boundary
   technique for the pilot.
6. ⚠ **Inside the Scaffold** — UNVERIFIED; cache-aware scaffold patterns → pilot compaction arms.
7. **GoodServe (2605.16867 ✓)** — agentic goodput (E2E-SLO completions/s); the throughput-side *dual*
   of our metric (`docs/metric-design.md`). Read methods + the router-side task-type inference.
8. ⚠ **Self-Harness** — UNVERIFIED; regression-gating / scaffold-churn rate.

Also worth adding (verified 2026-06-13): KVFlow (2507.07400), KVCOMM (2510.12872),
Helium (2603.16104), SparseX (2606.01751), More with Less (2510.16786).

**Industry / vendor (verified real online 2026-06-13 — read for landscape + methods; cite as
motivation only, never as research evidence):**
9. **NVIDIA Dynamo — agentic inference** (developer.nvidia.com/blog/full-stack-optimizations-for-agentic-inference-with-nvidia-dynamo)
   — KV-aware router + `nvext.agent_hints` spec. HIGH priority: bears directly on C4 (pre-emption) and
   the H1 framing (their 85–97% are *realized* hit rates under their own routing — a managed/realized
   reference point, NOT our infinite-cache "available" pole).
10. **AA-AgentPerf (Artificial Analysis)** (artificialanalysis.ai/articles/aa-agentperf) — methodology:
    agents/MW, SLO tiers, closed test set; bears on C1 distinctness + C3 (no public trace).
11. **FlashMemory-DeepSeek-V4 / Lookahead Sparse Attention** (2606.09079 ✓, Tencent et al.) — learned
    prediction of query-critical KV chunks. Read for **H3** (a learned version of "phase-aware retention"
    = prior art) + C2. Note: *intra-request* long-context, DeepSeek-V4-coupled, preliminary/suspended —
    not the multi-tenant/agentic-loop regime, and it does NOT touch C1.

**Metric anchors + newly-found competitors (verified 2026-06-14 — see `docs/metric-design.md`):**
12. **Cost-of-Pass** (2504.13359 ✓, ICLR 2026) — the economic-eval framework; academic anchor for
    cost-per-verified-task. Read first for the metric write-up.
13. **EET** (2601.05777 ✓) + **Efficient Agents** (2508.02694 ✓) — capability-side cost-of-pass /
    early-termination ("when to stop gritting"). + **TokenPowerBench** (AAAI ✓) — J/token energy.
14. **HexAGenT** (2605.16637 ✓) + **Cortex** (2510.14126 ✓) — workflow-aware agentic serving/scheduling
    (the "declared" side of the seam). Newly found; crowd the mechanism space further — read to position.
