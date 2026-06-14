# Agentic-Serving Characterization

> *How do agentic LLM workloads stress an inference server differently from chat — and what does that cost per unit of useful work?*

A measurement-and-characterization study of **agentic inference serving**. We quantify the
**realized-vs-available cache-locality gap** under realistic mixed (chat × agent) traffic and express
it as **cost per _verified_ iteration** — the *"Cost of Grit"* — using only **public benchmarks**
(SWE-bench Verified, τ²-bench) and **open infrastructure** (vLLM / SGLang).

Not a new system, recipe, or kernel — a rigorous, reproducible **measurement**.

- **Target:** MLSys 2027 Industry Track (~Oct 2026) — *provisional, pending CFP* ([`07-venues/venues.md`](07-venues/venues.md))
- **Status:** citation ledger complete · pilot design in review (open design issues gate GPU spend) · next step is the co-design / metric-redesign meeting, then the pilot cell
- **Start here:** [`STATUS.md`](STATUS.md) — the single source of "where are we"
- **New to the area?** [`docs/agentic-inference-brief.pdf`](docs/agentic-inference-brief.pdf) — an annotated study brief that summarizes every key paper in plain language (jargon explained, no shorthand)

---

## The problem

Chat is one prompt → one stream; its KV cache lives for a single turn. An **agent is a stateful loop**
(model → tool → model → …): context grows monotonically, the model is re-entered many times against a
mostly-shared prefix, the GPU idles during tool calls, and KV state becomes long-lived. Prefix caching
*should* make this cheap — **if the cache isn't evicted first**.

So: under realistic mixed traffic on a *bounded* cache, how much of the **available** reuse is actually
**realized**, what *drives* the gap, and what does it cost per useful (verified) unit of work? No one
has measured this cleanly on open infrastructure — that's the opening.

## Contributions

| | Contribution | Status |
|---|---|---|
| **C1** — *lead* | The **cost-per-verified-iteration / "Cost of Grit" curve** + the realized-vs-available **cache-locality gap**, quantified on open infra | pilot pending |
| **C3** — *artifact* | A released **mixed chat×agent, cost-labeled, OTel-format serving trace + harness** (no such public trace exists) | bundled with C1 |

Secondary and parked/pre-empted candidates (C2, C4, C6) live in
[`04-ideas/candidates.md`](04-ideas/candidates.md); killed ideas — with cause of death — in
[`04-ideas/graveyard.md`](04-ideas/graveyard.md). The discipline: **measurement, not mechanism**
(the eviction/TTL/sharing/scheduling space is crowded). Defensibility is the *bundle* —
rigor + breadth + open reproducibility + the trace artifact + precise framing.

## Hypotheses

Each is falsifiable with a stated kill criterion (full design in
[`05-experiments/pilot/README.md`](05-experiments/pilot/README.md)):

- **H1** — the locality gap is real on open infra, and multi-tenant **interleaving** is a *distinct* driver (separable from intra-agent churn).
- **H2** — cost-per-verified-iteration grows **super-linearly** with horizon and is cache-policy-sensitive.
- **H3** — tool-gap timing has exploitable **phase structure** that static eviction gets wrong.
- **H4** — a small public **trace + harness reproduces H1–H2** (artifact-as-contribution).

## The pilot — first, cheap, kill-fast

```
ReAct × τ²-bench × {isolated, mixed} × {LRU, retain-during-tool} × 50 scenarios × 3 repeats
= 600 trajectories on one vLLM config  (~1 week, <$300)
```

Readouts: available vs realized hit rate (**the gap**), cost-per-verified-iteration, tool-gap
distribution. The metric contract and the open design issues to settle before spending GPU budget are
in [`05-experiments/pilot/README.md`](05-experiments/pilot/README.md).

---

## Repository layout

```
STATUS.md                                ← current state, read first
docs/
  agentic-inference-brief.pdf / .html    Annotated study brief — every paper summarized (start here to learn the area)
  agentic-inference-primer.md            Serving mental model + the agentic frontier
  inference-systems-reading-map.md       Canonical inference-systems papers (verified arXiv IDs)
  threats-to-validity.md                 Reviewer-defense checklist + methods/artifact commitments
02-literature/
  sota-verified-2026.md                  Citation ledger — source of truth (✓ / ⚠)
  reading-queue.md                       Prioritized reading
  agentic-inference-survey.md            Survey            (placeholder)
  lit-review-short.md                    Condensed review  (placeholder)
  related-work-draft.md                  Related work      (placeholder)
04-ideas/
  candidates.md                          C1–C6 candidates (C1 "Cost of Grit" leads)
  graveyard.md                           Killed ideas — read before proposing new ones
05-experiments/pilot/
  README.md                              Pilot design + metric contract + open design issues
  experiments/matrix.yaml                Experiment matrix + the de-risking pilot cell
  harness/trace_schema.py                Metric contract (runs; smoke-tested)
  harness/run_pilot.py                   Orchestration skeleton (ownership seams)
06-collab/stakeholders.md                Co-authors + alignment
07-venues/venues.md                      Venue tracking
```

## Quick start

```bash
cd 05-experiments/pilot && python3 harness/trace_schema.py   # prints the derived metrics on a sample record
```
