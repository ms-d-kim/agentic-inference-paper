# Stakeholders & Alignment

- **Vinita** (kernel engineer, Together AI; co-author, ordering TBD). Historical drift toward
  optimization/mechanism framing vs measurement framing — resolved *by design* if C1 leads, since
  serving-side instrumentation (vLLM/SGLang internals, cache counters, interleaving load generation)
  is squarely her layer. **Next sync agenda:** (1) confirm C1 measurement framing is the lead;
  (2) pilot design review; (3) who owns instrumentation vs analysis; (4) authorship expectations,
  in writing.

- **NVIDIA (manager: Nick).** Summer scope being set. Keep this repo public-infra only. The
  product-side twin of C1 (metering, C5) is discussed at work and built internally if at all —
  never in this repo. **Open item:** one-line disclosure of the outside paper — sent / decided?
  Track the outcome here. This gates whether the repo can ever go public.

- **Faculty:** none attached (Tambe assessed a poor fit for the software-systems framing). Revisit
  only if a specific gap needs lab resources/compute. **(2026-06-14 flag:** Tambe's group just published
  *Agent Memory* (2606.06448) — now our closest characterization competitor. The faculty who passed is
  now adjacent prior art; note for positioning/etiquette.)

## IP / publication separation (standing constraint)
Two co-authors at companies that compete in inference (NVIDIA, Together). Mitigation built into the
design: public benchmarks + open infra (vLLM/SGLang) only, no proprietary stacks. Before anything
goes PUBLIC: each co-author clears their employer's publication-review process. Use personal
accounts/emails for commits on this side project.
