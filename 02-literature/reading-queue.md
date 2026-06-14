# Reading Queue (priority order)

*Carried from 2026-06-10. ⚠ flags added 2026-06-13 — several references are UNVERIFIED; see
`sota-verified-2026.md` before citing or quoting figures.*

1. ⚠ **AutoLab** §4.3 harness ablation — verify the "+0.43" magnitude/conditions. UNVERIFIED paper;
   do NOT quote the figure until confirmed. (blocks quoting it)
2. **Agent Memory** — ID 2606.06448 ✗ (likely wrong); a possible real "Agent Memory Below the Prompt"
   at ⚠ 2603.04428 (unverified). Confirm which, then read for affiliation/artifacts/scope vs serving loop.
3. ⚠ **SideQuest (2602.22603)** — UNVERIFIED; confirm it exists, then read eviction-policy details.
4. **Continuum / CacheTTL (2511.02230 ✓)** — repo README + any trace files; contents inventory.
5. **Don't Break the Cache (2601.06007 ✓, Lumer/PwC)** — methods section; reusable cache-boundary
   technique for the pilot.
6. ⚠ **Inside the Scaffold** — UNVERIFIED; cache-aware scaffold patterns → pilot compaction arms.
7. ⚠ **GoodServe** — UNVERIFIED; end-to-end-latency SLO formulation (prior art for loop-latency).
8. ⚠ **Self-Harness** — UNVERIFIED; regression-gating / scaffold-churn rate.

Also worth adding (verified 2026-06-13): KVFlow (2507.07400), KVCOMM (2510.12872),
Helium (2603.16104), SparseX (2606.01751), More with Less (2510.16786).

**Industry / vendor (verified real online 2026-06-13 — read for landscape + methods; cite as
motivation only, never as research evidence):**
9. **NVIDIA Dynamo — agentic inference** (developer.nvidia.com/blog/full-stack-optimizations-for-agentic-inference-with-nvidia-dynamo)
   — KV-aware router + `nvext.agent_hints` spec. HIGH priority: bears directly on C4 (pre-emption) and
   the H1 framing (their high single-session hit rates = the "managed/available" pole).
10. **AA-AgentPerf (Artificial Analysis)** (artificialanalysis.ai/articles/aa-agentperf) — methodology:
    agents/MW, SLO tiers, closed test set; bears on C1 distinctness + C3 (no public trace).
