# Discovery & gaps — agents in the wild, harness needs, and the benchmark↔production gap

*Two recurring questions, with an honest audit of what GRIT addresses, what it does not yet, and what to
do about it. External facts web-checked 2026-06-14.*

---

## Q1 — What do agents / harnesses / their developers actually need? (friction, time-to-first-token)

### What GRIT already addresses
- **The locality gap *is* a TTFT-and-cost story.** A surviving prefix-cache hit skips prefill → low
  time-to-first-token (TTFT); an evicted prefix → recompute → high TTFT **and** higher cost. So GRIT's
  headline (realized-vs-available reuse under mixed load) directly predicts how *predictable* an agent's
  TTFT and \$/task are when it shares an engine. That is a real harness pain, stated in serving terms.
- The **personas** in Figure 1 (platform eng, agent builder, FinOps) already name the felt pains.

### What GRIT does NOT yet address (the gaps)
1. **TTFT is implicit, not reported.** *Fix (cheap):* emit **TTFT and tail-TTFT (p50/p95)** as
   first-class pilot outputs next to cost-per-task. Same runs, far more developer-facing — "how much does
   the seam cost your *latency*, not just your bill."
2. **"Value of awareness" is underweighted.** How much a harness gains by *declaring* hints (resume-time,
   durable-prefix, fan-out markers) vs. staying engine-blind is literally "what reduces friction for
   harnesses." That is the C4 re-scope — promote it from afterthought to a measured axis if budget allows.
3. **Harness-developer pains are hypothesized, not validated.** The personas are reasoned, not interviewed.
   *Fix:* a short customer-discovery round (see Q2 "who to talk to"); the NVIDIA Dynamo role is the asset.
4. **Deployment friction proper is out of scope** (cold start, autoscaling, multi-LoRA, time-to-first-
   *deploy*). GRIT measures cache locality, not ops. Name it out-of-scope so we don't overclaim — it is
   the C5 product-twin's territory, not the paper's.

### Net
GRIT answers *"what does lost cache reuse cost an agent, and how unpredictable does it make TTFT/\$."*
It does **not** answer the full developer-experience / deployment-friction question. Adding TTFT outputs +
value-of-awareness + a few interviews covers most of the rest cheaply.

---

## Q2 — Is there a gap between agent benchmarks and production? Who to talk to?

### Yes, there is a gap.
Benchmarks (SWE-bench Verified, τ²-bench) are curated single tasks with synthetic arrival. Production is
concurrent, bursty, multi-tenant, long-tailed, with real tool latencies and retries. The serving community
built **BurstGPT / Azure traces precisely to bridge lab↔production for *chat*** — the *agent* equivalent
barely exists yet.

### How GRIT stands today
- **Partially addresses it:** C3 (release a mixed, cost-labeled trace) is the artifact answer to the gap.
- **But inherits it:** GRIT runs the *agent* arm on benchmarks, so it inherits "benchmark agent
  distribution ≠ production agent distribution." This must be a named threat, not a silent assumption.

### The concrete fix (improves realism *and* the contribution)
- **Drive the chat co-tenant with a *real* trace** (BurstGPT / Azure LLM Inference) instead of synthesizing
  it — so the mixed-arm interference is production-realistic. This is the strongest possible test of H1
  ("is interleaving the driver?") because the interfering load is real, not invented.
- **Keep the agent arm on benchmarks** (you need verifiable task success for the cost-per-*verified*-task
  denominator), but additionally **replay a real agent trace** (the vLLM × Mooncake Codex / SWE-bench-Pro
  corpus) for the *cache-behavior* half even where task success can't be re-verified.

### Who to talk to (to understand agents in the wild)
- **Inside NVIDIA (biggest asset):** the Dynamo PM/eng and the customer/solutions teams who see real agent
  serving workloads; NVIDIA inference customers.
- **Inference vendors / serving teams:** Together (Vinita), Fireworks, Baseten, Anyscale, Modal — they
  serve agents and see the real chat×agent traffic mix.
- **Agent product companies (the harnesses themselves):** Anysphere/Cursor, Cognition/Devin, All Hands
  AI/OpenHands, Replit, Factory, Sourcegraph/Amp, Windsurf — for harness + developer pain and willingness
  to pay.
- **Orchestration maintainers:** LangChain/LangGraph, CrewAI, LlamaIndex.
- **Observability vendors (aggregate in-the-wild telemetry):** LangSmith, Braintrust, Arize, Helicone,
  W&B Weave.
- **Trace authors / academia:** Moonshot (Mooncake), the BurstGPT / Azure-trace authors, the
  KVCache-in-the-Wild authors.

---

## Public traces available now (web-checked 2026-06-14)

| Trace | What it is | Real prod? | Agentic? | Cost-labeled? | Use for GRIT |
|---|---|---|---|---|---|
| **BurstGPT** (`2401.17644`) | 10.31M Azure-OpenAI requests over 213 days | yes | no (chat) | no | the realistic **chat co-tenant** |
| **Azure LLM Inference Traces** | 1-hr Azure traces, coding + conversation | yes | partial (coding) | no | co-tenant + arrival dynamics |
| **Mooncake conv. trace** (`2407.00079`) | KVCache-centric serving trace | yes | no | no | arrival / cache realism |
| **vLLM × Mooncake agent corpus** | 610 Codex / SWE-bench-Pro agent traces | yes | yes (agent-only) | no | **replay agent cache behavior** |
| **AgentServeSim** (`2606.09613`) | simulator + mini-swe-agent tool-call traces | captured/sim | yes | partial | scaffold / cross-check |
| **Agentic AI Workload Characteristics** (`2605.26297`) | agent workload measurements | yes | yes | no | characterization prior art |

**The empty cell still stands:** none is *mixed chat+agent **and** cost-labeled **and** open-infra **and**
OTel-format*. So C3's niche holds — but GRIT should **ingest** BurstGPT/Azure (chat side) + the vLLM×Mooncake
corpus (agent side) rather than synthesize, which both improves realism and reframes C3 as "the missing
*combination*," not "yet another trace."

---

## Actions (ingestible into the pilot / threats / ledger)
1. Add **TTFT + tail-TTFT** as first-class pilot outputs (`metric-design.md`, `harness/trace_schema.py`).
2. Use **BurstGPT / Azure** as the chat co-tenant in the mixed arm (`matrix.yaml`, threats).
3. Promote **value-of-awareness / hints** (C4) to a measured axis if budget allows.
4. Add a **"benchmark agent distribution ≠ production"** threat to `threats-to-validity.md`.
5. Run **~5–8 customer-discovery interviews** (harness devs + serving teams) to validate the personas; log.
6. Add **BurstGPT (`2401.17644`)** + **Azure LLM Inference Traces** to the citation ledger (web-verified
   2026-06-14) — they are the realistic-chat-trace prior art GRIT builds its co-tenant on.
