# Agentic-Serving Characterization — Working Repo

A measurement-and-characterization study of how agentic inference workloads differ structurally from
chat, and what that means for serving-system design. Public benchmarks (SWE-bench Verified, τ²-bench)
+ open infra (vLLM/SGLang) only. Target: **MLSys 2027 Industry Track (~Oct 2026)**.

**Start with [`STATUS.md`](STATUS.md).** It is the reconciled current state and overrides the older
planning doc.

## Layout
```
docs/agentic-inference-primer.md     Expert primer + canonical reading list
02-literature/
  sota-verified-2026.md              Citation source of truth (✓/⚠ verification status)
  reading-queue.md                   Prioritized reading (unverified refs flagged)
  *-PLACEHOLDER.md                   Prior-session artifacts to paste back in
04-ideas/
  candidates.md                      C1–C6 (C1 "Cost of Grit" is the lead)
  graveyard.md                       Killed ideas — read before proposing anything new
05-experiments/pilot/
  README.md                          Pilot design doc = the Vinita-sync artifact
  experiments/matrix.yaml            Experiment cross-product + the de-risking pilot cell
  harness/trace_schema.py            Metric contract (runs; smoke-tested)
  harness/run_pilot.py               Orchestration skeleton with ownership seams
06-collab/stakeholders.md            Vinita / NVIDIA / faculty + IP separation
07-venues/venues.md                  Venue tracking
```

## Quick check
```bash
cd 05-experiments/pilot && python3 harness/trace_schema.py   # prints derived metrics
```

## On GitHub — recommended: PRIVATE first, public only at release
GitHub is the right home for version control, collaborating with Vinita, and eventually releasing
the trace + harness (that public release IS contribution C3). But **keep the repo private during
development**, for reasons specific to this project:

1. **Employer publication review / IP separation.** Two co-authors at companies that compete in
   inference (NVIDIA, Together AI). A public repo is a form of disclosure. Before going public, each
   co-author should clear their employer's publication-review process; confirm the NVIDIA outside-
   paper disclosure first (`06-collab/stakeholders.md`). *Not legal advice — check the actual policies.*
2. **Don't hand the gap to faster teams.** The space is hot and closing. A public repo broadcasting
   H1–H4 and the trace plan to exactly the groups (Berkeley/Sky, MSR, Alibaba, …) who could execute
   faster helps a competitor more than a timestamp helps you. A dated arXiv post protects priority
   better than an early public repo.
3. **Keep it clean for the eventual public release.** The design is already public-infra/public-
   benchmark only — keep it that way. The NVIDIA product twin (C5 metering) stays out entirely.
4. **Commit hygiene.** Use a personal account/email (not employer identity) for this side project.
   Never commit secrets or large trace files (`.gitignore` covers both).

Suggested flow:
```bash
git init && git add . && git commit -m "Initial: primer, SOTA ledger, pilot scaffold"
git remote add origin git@github.com:<you>/agentic-inference-paper.git   # PRIVATE repo
git push -u origin main
```
Flip to public at/after arXiv submission, once both employers have signed off.
