# Stakeholders & Alignment

- **Vinita** (kernel engineer, Together AI; co-author, ordering TBD). Historical drift toward
  optimization/mechanism framing vs measurement framing — resolved *by design* if C1 leads, since
  serving-side instrumentation (vLLM/SGLang internals, cache counters, interleaving load generation)
  is squarely her layer. **Next sync agenda:** (1) confirm C1 measurement framing is the lead;
  (2) pilot design review; (3) who owns instrumentation vs analysis; (4) authorship expectations,
  in writing.

- **NVIDIA (manager: Nick).** Summer internship — the product / customer-discovery side. The metering
  twin of C1 (C5) is the work-side product angle, distinct from this open measurement paper.

- **Faculty:** none attached (Tambe assessed a poor fit for the software-systems framing). Revisit
  only if a specific gap needs lab resources/compute. **(2026-06-14 flag:** Tambe's group just published
  *Agent Memory* (2606.06448) — now our closest characterization competitor. The faculty who passed is
  now adjacent prior art; note for positioning/etiquette.)

## Scope note
Public benchmarks + open infra (vLLM/SGLang) only — a design choice for **reproducibility**, not for any
other reason.
