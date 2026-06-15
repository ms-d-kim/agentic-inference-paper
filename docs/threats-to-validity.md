# Threats to Validity & Methods Commitments

*Reconciled from the 13 Jun 2026 working brief (§7, §9–10). Reviewer-defense checklist + standing
commitments to carry into the methods section and the artifact release. Items already covered
elsewhere are cross-referenced rather than restated.*

## Validity (these decide whether the result means anything)

1. **The model-vs-system boundary is the #1 threat to validity.** Many quantities — tool-calling
   efficiency, reasoning length, iteration count, even task success — are functions of the *model*, not
   the serving system. Attributing them to serving knobs invalidates the contribution. **Commitment:**
   hold the model fixed, vary only serving configuration, and explicitly bound which effects are
   model-driven. Make this a methods-section commitment. (cf. primer Part E #4; matrix.yaml fixes one
   model family for V1.)

2. **Prove the interleaving mechanism (H1); don't assume it.** Sutradhara attributes cache collapse to
   intra-request churn + eviction, not multi-tenancy. The contribution depends on isolating the
   *tenancy* contribution — design the isolated-vs-mixed contrast so the attribution is clean. (cf.
   [`../05-experiments/pilot/README.md`](../05-experiments/pilot/README.md) H1 + kill criterion;
   [`../02-literature/sota-verified-2026.md`](../02-literature/sota-verified-2026.md) critical nuances.)

3. **Statistical rigor decides whether the pilot means anything.** The kill criteria depend on the gap
   exceeding noise. **Commitment:** budget enough repeats, report variance / confidence intervals, and
   **pre-register the effect size** you'd call meaningful before running. (Pilot is 3 repeats × 50
   scenarios; pre-registration is the gap not yet captured in the pilot doc.)

## Benchmarks & artifact (mostly new — not captured elsewhere)

4. **Benchmark licensing & currency.** SWE-bench Verified and LiveCodeBench are MIT-licensed; **confirm
   τ²-bench's license** before release. Prefer contamination-resistant sets (SWE-bench Pro) for
   currency. **Pin and document benchmark versions.**

5. **Artifact / reproducibility norms.** Systems venues value artifact evaluation. The released trace +
   harness (C3) should **target artifact badging**: pin engine versions, seeds, and environment;
   license the **trace** permissively (e.g. CC-BY) and the **harness** (e.g. Apache-2.0 / MIT); document
   the collection method end-to-end.

6. **Trace-release hygiene.** Ensure no PII or proprietary content in any released trace
   (public-benchmark-only scope helps). Document exactly how it was collected and labeled. (cf.
   `.gitignore` already blocks raw traces from accidental commit; this is the release-time commitment.)

## Strategy & process (cross-referenced; the gates around the work)

7. **Author order is substantive.** Instrumentation is the credibility-critical layer and is Vinita's;
   the framing plausibly moves her to co-first. Decide a *proposed* order before the sync rather than
   improvising. (cf. pilot README ownership split.)

8. **Fast-follower risk.** The area is hot and closing. A dated arXiv post + the public artifact protect
   priority better than a stealth repo or a deadline-driven scramble. (cf.
   [`../07-venues/venues.md`](../07-venues/venues.md).)

9. **Don't cite vendor headline numbers** (model-launch blogs, SWE-bench Pro marketing figures) as
   research evidence — use the paper plus your own measurement. (cf. primer Part E #5.)

## Confounds the design must control (added 2026-06-14, external Codex pass)

*These were absent and are the ones most likely to invalidate the result. Each must map to a controlled
variable, a randomized variable, or an admitted limitation in the methods section.*

10. **Saturation / provisioning regime.** The seam only bites under bounded cache + pressure; if the box is
    well-provisioned the gap vanishes. Pre-register the KV-pressure regimes (#4) and report where the effect
    appears and disappears — don't report a single operating point as "the" result.
11. **Chat-tenant SLO harm.** The mixed arm can degrade the *chat* co-tenant's latency/SLO; an agent "win"
    paid for by chat regressions is not a win. Measure and report both tenants' SLOs.
12. **Synthetic-mixture validity.** Benchmark agents + a synthetic chat stream have no real joint arrival
    correlations or shared-prefix structure; the "mixed" workload may not resemble production. Drive the chat
    co-tenant from a *real* trace (BurstGPT/Azure, cf. `discovery-and-gaps.md`) and state the residual gap.
13. **Instrumentation & engine-patch perturbation.** The block-owner attribution patch (observability §1)
    and added logging change timing/throughput — the act of measuring perturbs the thing measured. Quantify
    overhead; run the headline cost numbers on an *un-patched* build and use the patched build only for
    attribution.
14. **Quantization, cache-block size, routing affinity, replica placement.** Each silently moves realized
    hit rate and cost. Pin and report them; treat block size and quantization as fixed (or as declared
    sub-studies), not free.
15. **Timeout / censoring bias.** Horizon caps and wall-clock timeouts censor long trajectories; cost-per-
    verified-task is sensitive to where the cap falls. Pre-register caps and report a censoring/survival curve.
16. **Scaffold selection.** Swapping to a "stronger scaffold" to lift the resolve-rate floor (#14) changes
    the very workload whose cache behavior is measured. Fix the scaffold or treat scaffold as an explicit axis.
17. **Multiple comparisons.** The matrix is a grid of cells × policies × engines × horizons; un-corrected
    per-cell tests will manufacture "significant" effects. Pre-register the primary contrast; correct the rest.
18. **Benchmark-oracle error.** `FAIL_TO_PASS` / τ²-success oracles have false positives/negatives that feed
    the denominator directly. Spot-audit verified outcomes; report oracle error as a denominator uncertainty.
