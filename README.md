# Agentic-Serving Characterization

A measurement-and-characterization study of how agentic inference workloads differ structurally from
chat, and what that means for serving-system design. Public benchmarks (SWE-bench Verified, τ²-bench)
+ open infra (vLLM/SGLang) only. Target: **MLSys 2027 Industry Track (~Oct 2026)** — provisional,
pending the 2027 CFP (see [`07-venues/venues.md`](07-venues/venues.md)).

See [`STATUS.md`](STATUS.md) for current state.

## Layout
```
docs/agentic-inference-primer.md         Expert primer + mental model + agentic frontier
docs/inference-systems-reading-map.md    Canonical inference-systems reading map (verified IDs)
docs/threats-to-validity.md              Reviewer-defense checklist + methods/artifact commitments
02-literature/
  sota-verified-2026.md              Citation source of truth (✓/⚠ verification status)
  reading-queue.md                   Prioritized reading (unverified refs flagged)
  agentic-inference-survey.md        Survey (placeholder — paste prior-session text)
  lit-review-short.md                Condensed lit review (placeholder)
  related-work-draft.md              Related-work draft (placeholder)
04-ideas/
  candidates.md                      C1–C6 (C1 "Cost of Grit" is the lead)
  graveyard.md                       Killed ideas — read before proposing anything new
05-experiments/pilot/
  README.md                          Pilot design doc
  experiments/matrix.yaml            Experiment cross-product + de-risking pilot cell
  harness/trace_schema.py            Metric contract (runs; smoke-tested)
  harness/run_pilot.py               Orchestration skeleton with ownership seams
06-collab/stakeholders.md            Co-authors + IP separation
07-venues/venues.md                  Venue tracking
```

## Quick check
```bash
cd 05-experiments/pilot && python3 harness/trace_schema.py   # prints derived metrics
```
