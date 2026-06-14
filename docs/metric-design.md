# Metric Design — the "Cost of Grit" (resolves pilot open-issues #1 and #5)

*Decision doc for the co-design sync. Settles how the headline metric is defined, denominated, and
computed. Supersedes the looser definitions in `05-experiments/pilot/README.md` and the brief once
ratified by both authors.*

## Decision (proposed)

**Headline = cost per verified _task_, reported as a curve, group-level.**

- **Denominator — the verified task** (not the iteration). Count a task as verified by its benchmark
  oracle (SWE-bench `FAIL_TO_PASS`, τ²-bench success); for long-horizon tasks allow **partial credit**
  (SWE-EVO-style "Fix Rate") so the signal isn't all-or-nothing.
- **Numerator — resource cost, three units, GPU-seconds primary.**
  - **GPU-seconds** = the reproducible scientific currency (hardware/price-neutral). *Primary.*
  - **Dollars** = the buyer-facing view, reported with a *stated* price (provider/pricing-confounded —
    never primary; this is the trap [Don't Break the Cache] falls into at the API level).
  - **Joules / "verified tasks per kWh"** = the TCO + sustainability view (the established unit is
    J/token — see TokenPowerBench); connects to AA-AgentPerf's per-megawatt framing. Report when power
    telemetry is available; **include CPU tool-processing energy** (the CPU-Centric paper shows it is
    non-trivial).
- **Count the cost of failed attempts.** Cost per verified task = (total cost over *all* attempts on a
  task family) ÷ (verified tasks). Charging only successes drops the expensive long-horizon failures —
  exactly where grit's cost lives (the survivor bias, open-issue #5). This requires an attempt/retry
  record in the trace (open-issue #8).
- **Always a curve, never a scalar.** Plot against **horizon × cache policy × tenancy**. The whole
  thesis is *super-linearity*; a single number hides it.

## Why this, grounded in SOTA

The field measures efficiency in three disconnected camps; our metric is the missing bridge.

| Camp | What it measures | Representative work |
|---|---|---|
| Serving / capacity | useful **throughput** under an SLO (goodput) | **GoodServe** (agentic goodput = E2E-SLO completions/s; 2605.16867), AA-AgentPerf (agents/MW), InferenceMAX (tokens/s, $/token) |
| Capability / economics | **cost per correct task** at the API black box | **Cost-of-Pass** (expected $ for a correct solution, ICLR 2026, 2504.13359), Efficient Agents (2508.02694), More with Less, EET (2601.05777) |
| Sustainability | **energy per output** | TokenPowerBench (J/token) |

- **"Cost-of-Pass" is the academic name for our denominator** — expected cost of a *correct* solution,
  built on Farrell's productive-efficiency theory. We adopt it, but move it **from the API black box
  into open serving internals** and tie its cost term to the **locality gap**. That move is the novelty.
- **Cost-of-Grit is the economic _dual_ of goodput.** Goodput = useful work per *second* under an SLO
  (what GoodServe optimizes). Cost-of-Grit = useful work per *resource* (GPU-s / J / $). Framing it as
  "goodput, priced, for agents" anchors it in an accepted metric and differentiates us from GoodServe:
  they *optimize* throughput with a router; we *measure* cost-per-verified-task and *attribute* it to
  cache locality on open infra.

## The decomposition (what makes it a _serving_ result, not another cost-of-pass)

```
cost per verified task  ≈  (cost per iteration) × (iterations per task) ÷ (success rate)
```

Cost-of-Pass / Efficient Agents / EET measure the whole thing at the API level (capability side). Our
contribution is to **open the box**: attribute the **cost-per-iteration** term to the realized-vs-
available **locality gap**, and show how the gap inflates it as the context grows — turning a capability
number into a serving result with an actionable knob (the cache policy).

## The one figure (the thesis in one plot)

x-axis = horizon; three curves:
1. **$/token** — nearly flat (the misleading framing the paper debunks).
2. **cost / iteration** — rising.
3. **cost / verified task** — rising **super-linearly**.

The gap between curve 1 and curve 3 *is* the Cost of Grit; the portion attributable to eviction *is* the
locality tax. (See also: cost-per-verified-task **at matched success rate** across cache policies, to
strip out model-driven capability differences.)

## Explicitly rejected / relegated

- **Per token** as the outcome unit — the strawman the paper exists to debunk ("cheapest per token ≠
  cheapest per task"). Keep only as the contrast baseline (curve 1).
- **Per iteration** as the *headline* — demote to the diagnostic decomposition term (a gritty agent that
  takes many cheap steps looks "cheap per iteration," hiding the grit).
- **"Useful actions per watt"** — "useful action" needs gold labels (subjective, model-driven); and
  "per watt" is *power/capacity*, not *energy/cost* (that's AA-AgentPerf's question). If we want the
  energy lens it's **verified tasks per kWh** (= Joules per verified task), not actions/watt.

## Confounds this commits us to (methods section)

1. **Model vs. system** — hold the model fixed; report cost-per-verified-task *as a frontier or at
   matched success rate* so serving never gets credit for capability.
2. **Failed-attempt accounting** (#5) + the attempt/retry trace record (#8).
3. **Verification definition** pinned per benchmark + the partial-credit rule, pre-registered.
4. **Energy telemetry** caveats (rented-GPU power draw; CPU tool energy); GPU-seconds stays the anchor.

## What this resolves / leaves open

- **Resolves open-issue #1** (locality_gap = available − realized on a *common eligible-token
  denominator*, clamped to [0,1]) and **#5** (failed-attempt cost).
- **Depends on #8** (attempt/retry + cost-attribution record) to be implementable.
- **Open for the sync:** the exact partial-credit rule for long-horizon tasks; the dollar price used for
  the $ view; whether to report energy in V1 or defer to V2.
