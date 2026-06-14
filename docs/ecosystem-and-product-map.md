# Agentic-Serving — Ecosystem & Product Map

*The **product / business lens** that the measurement paper sits inside — ecosystem players, personas,
journeys, pains, and opportunities. This is a **companion**, not part of the paper's scientific claims
(the paper is the open measurement; this map is the market/product view, useful for the NVIDIA-product
/ customer-discovery side). Diagrams are Mermaid (renders on GitHub); see the format note at the bottom
for richer/interactive options.*

---

## 1. Ecosystem — the relational map (who builds on / competes with / measures whom)

```mermaid
flowchart TB
  subgraph APP["Agent apps & products"]
    AC["Coding agents (Cursor, Claude Code, Codex, OpenHands)"]:::app
    AW["Web / computer-use / research agents"]:::app
  end
  subgraph ORC["Orchestration layer (drives the loop)"]
    LG["LangGraph · CrewAI · OpenAI Agents SDK · AutoGen"]:::orc
  end
  subgraph ENG["Serving engines (run the model)"]
    VLLM["vLLM"]:::eng
    SGL["SGLang"]:::eng
    KVINFRA["KV infra: Mooncake · LMCache · llm-d"]:::eng
  end
  subgraph VEND["Vendors / hardware / stacks"]
    DYN["NVIDIA Dynamo + GPUs"]:::vend
    AMD["AMD · Google TPU"]:::vend
  end
  subgraph MEAS["Benchmarks & measurement"]
    AAP["AA-AgentPerf (agents/MW)"]:::meas
    IX["SemiAnalysis InferenceX ($/token)"]:::meas
    BENCH["SWE-bench · τ²-bench · HAL"]:::meas
  end
  US["THIS PROJECT — the open 'meter':<br/>cost-per-verified-task + public mixed trace"]:::us

  AC --> LG
  AW --> LG
  LG -->|"the seam: workflow-agnostic;<br/>declared vs inferred"| VLLM
  LG --> SGL
  VLLM --> DYN
  SGL --> DYN
  KVINFRA --> VLLM
  KVINFRA --> SGL
  DYN -. competes .- AMD
  AAP -. measures .-> DYN
  IX -. measures .-> ENG
  BENCH -. scores .-> APP
  US -. "measures the seam<br/>on open infra, by cost-per-task" .-> ENG
  US -. "fills the gap none of these cover" .-> MEAS

  classDef app  fill:#E8EEF7,stroke:#33527A,color:#13243B;
  classDef orc  fill:#EDEFF2,stroke:#5A6473,color:#1E2632;
  classDef eng  fill:#E3F0EC,stroke:#2E6F5E,color:#10302A;
  classDef vend fill:#FBF3E0,stroke:#9A7B27,color:#3D3210;
  classDef meas fill:#EFEAF6,stroke:#5B4A8A,color:#241C3A;
  classDef us   fill:#E7F0FA,stroke:#1F4E79,stroke-width:2px,color:#0E2A45;
```

**The takeaway the map encodes:** value flows top-down (apps → orchestration → engines → hardware); the
**seam** (orchestration ↔ engine) is where reuse is lost; everyone is piling into *mechanisms* (engines,
Dynamo, KV infra) and *vendor benchmarks* (AA-AgentPerf, InferenceX) — but **no one occupies the open,
cost-per-completed-task measurement of the seam.** That's where this project sits.

## 2. Bird's-eye mindmap

```mermaid
mindmap
  root((Agentic serving ecosystem))
    Hardware and vendors
      NVIDIA Dynamo and GPUs
      AMD and Google TPU
    Serving engines OSS
      vLLM
      SGLang
      Mooncake LMCache llm-d
    Orchestration frameworks
      LangGraph
      CrewAI
      OpenAI Agents SDK
    Benchmarks and measurement
      AA-AgentPerf agents per megawatt
      SemiAnalysis InferenceX cost per token
      SWE-bench and tau2-bench and HAL
    Research labs
      Berkeley Sky and MSR
      Alibaba and SJTU and Stanford
    Personas
      Platform serving engineer
      Agent product builder
      ML systems researcher
      Eng leadership and FinOps
    Pain points
      Cost grows with horizon
      Cache misses under shared traffic
      No cost per task visibility
      Orchestrator engine seam
    Opportunities
      Cost per verified task meter
      Public mixed trace
      Hint contract declared vs inferred
```

## 3. Personas

| Persona | Who they are | Goal | What they care about | Pain today |
|---|---|---|---|---|
| **Platform / serving engineer** | infra team at an AI-infra co or a Dynamo customer | serve agents cheaply at the SLO | goodput, $/GPU-hour, cache hit rate | can't explain *why* agents cost ~5× chat; co-locating chat+agents spikes cost and they can't see why |
| **Agent product builder / startup** | building a coding or workflow agent | viable unit economics | cost per *completed* task, latency, margins | cost blows up at long horizons; $/token looks fine but $/task explodes; no visibility into where it goes |
| **ML-systems researcher** | serving / KV-cache research | publish, compare fairly | reproducibility, a standard metric, a public trace | no public agentic+cost-labeled trace; can't compare engines/configs apples-to-apples |
| **Eng leadership / FinOps** | owns the inference budget | forecast & control spend | $/outcome, predictability | unpredictable token bills; no "cost per successful task" meter to budget against |
| **Inference-vendor PM** *(the internship's customer lens)* | NVIDIA / a serving vendor | make the stack the best for agents | which agentic pains are biggest & most monetizable | doesn't have an open, neutral measurement of where the cost actually goes |

## 4. User journeys (pain in motion)

1. **The surprise bill** *(agent startup)* — usage scales; the token bill 4×s. Per-token price is unchanged, but **cost per completed task exploded at long horizons** and no tool shows why. → *needs the cost-of-grit meter.*
2. **The platform team's blind spot** *(infra eng)* — they co-locate chat + agents to save GPUs; agent latency/cost spikes; they *suspect* cache eviction but the engine only exposes an **aggregate** hit rate, not "did chat evict *this agent's* cache." → *needs per-tenant attribution + the locality-gap metric.*
3. **The apples-to-oranges comparison** *(researcher)* — wants vLLM vs. SGLang for agents; there's **no public mixed trace** and **no standard cost-per-task metric**, so every paper measures differently. → *needs the open trace + the metric standard.*

## 5. Pain → Opportunity map

| Pain (market) | Opportunity | Who captures it | This project? |
|---|---|---|---|
| Cost grows super-linearly with horizon, hidden by $/token | **The "meter": cost-per-verified-task** (the locality-tax curve) | researchers + FinOps + vendors | ✅ **C1 (the paper)** |
| Cache reuse collapses under shared / bounded cache | quantify **realized-vs-available gap**; the *value of awareness* | serving teams | ✅ **C1 / H1** |
| No per-tenant cost/eviction visibility | **instrumentation + attribution methodology** | platform teams, vendor (Dynamo) | partial (paper measures; product builds) |
| Orchestrator↔engine seam (declared vs inferred) | a **hint contract / standard** | vendors (Dynamo), llm-d/Gateway | ⚠️ pre-empted (Dynamo); *measure its value* |
| No public agentic + cost-labeled trace | **release the trace** | the commons | ✅ **C3 (the artifact)** |
| Can't compare engines/configs fairly | reproducible **open-infra benchmark + metric** | the commons | ✅ bundled with C1/C3 |

**Where this project plays vs. the product side:** the **open measurement** (the meter + the trace, rows
marked ✅) is the *paper*. The **productized** versions — building the meter into Dynamo / a FinOps SaaS,
shipping the hint contract — are the *product/internship* side (the "C5" twin), deliberately out of the
paper's scope.

---

## Format note — best way to present this
- **In-repo, versioned, reviewable (what this file is):** Mermaid in Markdown — renders on GitHub, diffs
  cleanly, lives next to the work. Best for a map you'll iterate on with a co-author.
- **Mermaid `mindmap`** (section 2) = the brainstorm/taxonomy view; **Mermaid `flowchart`** (section 1) =
  the relational "who-relates-to-whom" view. Tables beat diagrams for personas/journeys/pains.
- **For a truly interactive / clickable / movable map** (workshop-style), a dedicated canvas —
  FigJam / Miro / Whimsical / Excalidraw — is better than Mermaid; export a PNG back here to version it.
- I can also generate a **self-contained interactive HTML** (zoomable nodes, hover details) on request.
