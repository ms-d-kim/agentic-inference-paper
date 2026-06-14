# Canonical Inference Systems — Reading Map

*Reconciled from the 13 Jun 2026 working brief (§5). This is the map of the inference-systems field
your serving work sits inside: the load-bearing papers on serving, KV cache, caching, attention
kernels, parallelism, quantization, and decoding. Every arXiv ID below was checked against arXiv /
venue records on 2026-06-13 (✓). Companion to [`agentic-inference-primer.md`](agentic-inference-primer.md)
(mental model + agentic frontier) and [`../02-literature/sota-verified-2026.md`](../02-literature/sota-verified-2026.md)
(the agentic-serving competitive set). Use this to fill gaps; the frontier builds directly on these.*

**The one organizing idea:** inference has two regimes — **prefill** is compute-bound, **decode** is
memory-bandwidth-bound — and almost everything here is either (a) moving work across that
compute/bandwidth line, or (b) managing the **KV cache** (its size, reuse, eviction, precision, or
placement). Read each paper by asking which of those two it does.

---

## Foundations & the inference mental model
| Paper | arXiv / venue | What it is |
|---|---|---|
| Attention Is All You Need — Vaswani et al. (NeurIPS'17) | 1706.03762 ✓ | the transformer; the substrate everything below optimizes |
| Efficiently Scaling Transformer Inference — Pope et al. (MLSys'23) | 2211.05102 ✓ | the inference roofline: analytical partitioning model, MFU, why MQA scales — **read this first** |

## Serving systems & scheduling
| Paper | arXiv / venue | What it is |
|---|---|---|
| Orca — Yu et al. (OSDI'22) | no arXiv ✓ | continuous (iteration-level) batching + selective batching |
| PagedAttention / vLLM — Kwon et al. (SOSP'23) | 2309.06180 ✓ | OS-style paging of the KV cache; the open serving baseline |
| Sarathi-Serve — Agrawal et al. (OSDI'24) | 2403.02310 ✓ | chunked prefill + stall-free batching |
| SGLang / RadixAttention — Zheng et al. (NeurIPS'24) | 2312.07104 ✓ | radix-tree prefix-cache reuse + structured-output FSM |
| AlpaServe — Li et al. (OSDI'23) | 2302.11665 ✓ | statistical multiplexing via model parallelism under bursty load |

## Prefill / decode disaggregation
| Paper | arXiv / venue | What it is |
|---|---|---|
| DistServe — Zhong et al. (OSDI'24) | 2401.09670 ✓ | split prefill and decode onto different GPUs for goodput |
| Splitwise — Patel et al. (ISCA'24) | 2311.18677 ✓ | phase splitting across machine types; cheaper/greener decode |
| Mooncake — Qin et al. (Moonshot, 2024) | 2407.00079 ✓ | KVCache-centric disaggregation; the stack behind Kimi |

## Attention efficiency & kernels
| Paper | arXiv / venue | What it is |
|---|---|---|
| FlashAttention — Dao et al. (NeurIPS'22) | 2205.14135 ✓ | IO-aware exact attention: linear memory, large speedup |
| FlashAttention-2 / -3 — Dao et al. | 2307.08691 / 2407.08608 ✓ | better work-partitioning; Hopper asynchrony + low precision |
| Multi-Query Attention — Shazeer (2019) | 1911.02150 ✓ | one KV head for all query heads; shrinks the KV cache |
| Grouped-Query Attention — Ainslie et al. (2023) | 2305.13245 ✓ | the MQA/MHA middle ground used by most modern models |
| FlashInfer — (MLSys'25) | 2501.01005 ✓ | customizable attention kernels for serving engines |

## KV cache compression / management
| Paper | arXiv / venue | What it is |
|---|---|---|
| StreamingLLM (attention sinks) — Xiao et al. (ICLR'24) | 2309.17453 ✓ | keep initial-token "sinks" + a recent window for streaming |
| H2O (heavy-hitter oracle) — Zhang et al. (NeurIPS'23) | 2306.14048 ✓ | evict KV by attention-score importance |
| KIVI — Liu et al. (2024) | 2402.02750 ✓ | tuning-free 2-bit KV cache quantization |

## Caching & reuse
| Paper | arXiv / venue | What it is |
|---|---|---|
| Prompt Cache — Gim et al. (MLSys'24) | 2311.04934 ✓ | modular precomputed attention reuse across requests |
| *(see also, the agentic frontier)* | — | RadixAttention, KVFlow, KVCOMM, Continuum/CacheTTL, Don't Break the Cache — in [`../02-literature/sota-verified-2026.md`](../02-literature/sota-verified-2026.md) |

## Parallelism (training-era ideas that carry to inference)
| Paper | arXiv / venue | What it is |
|---|---|---|
| Megatron-LM — Shoeybi et al. (2019) | 1909.08053 ✓ | tensor (intra-layer) model parallelism |
| Megatron on GPU clusters — Narayanan et al. (SC'21) | 2104.04473 ✓ | composing tensor + pipeline + data parallelism |
| GPipe — Huang et al. (NeurIPS'19) | 1811.06965 ✓ | pipeline parallelism with micro-batching |
| ZeRO — Rajbhandari et al. (SC'20) | 1910.02054 ✓ | shard optimizer/grad/params (the basis of FSDP) |
| Ring Attention — Liu et al. (2023) | 2310.01889 ✓ | sequence/context parallelism for near-infinite context |

## Quantization
| Paper | arXiv / venue | What it is |
|---|---|---|
| LLM.int8() — Dettmers et al. (2022) | 2208.07339 ✓ | 8-bit matmul with outlier handling |
| GPTQ — Frantar et al. (2022) | 2210.17323 ✓ | one-shot 3–4 bit weight quantization (2nd-order) |
| SmoothQuant — Xiao et al. (ICML'23) | 2211.10438 ✓ | migrate activation outliers to weights for W8A8 |
| AWQ — Lin et al. (MLSys'24) | 2306.00978 ✓ | activation-aware weight quantization |

## Speculative decoding
| Paper | arXiv / venue | What it is |
|---|---|---|
| Speculative decoding — Leviathan et al. (ICML'23) | 2211.17192 ✓ | draft + verify; exact-distribution speedup |
| Speculative sampling — Chen et al. (DeepMind, 2023) | 2302.01318 ✓ | concurrent formulation of the same idea |
| Medusa — Cai et al. (ICML'24) | 2401.10774 ✓ | multiple decoding heads, no separate draft model |
| EAGLE — Li et al. (ICML'24) | 2401.15077 ✓ | feature-level autoregressive drafting |
| Lookahead decoding — Fu et al. (2024) | 2402.02057 ✓ | break the sequential dependency without a draft model |

---

## Unknown unknowns — make sure you can explain each of these

1. **The roofline / arithmetic-intensity model** (Pope et al.). Decode is bandwidth-bound (low
   intensity); prefill is compute-bound; batching raises intensity. If you can't place a technique on
   the roofline, you don't yet understand *why* it helps.
2. **The memory wall.** In decode, loading weights + KV from HBM dominates wall-clock, not FLOPs.
   That's why a forward over K tokens costs ~the same as over 1 — the entire basis of speculative decoding.
3. **Goodput, not throughput.** The SLO-meeting metric. Disaggregation (DistServe/Splitwise/Mooncake)
   is fundamentally a goodput play — and so is our cost-per-verified-iteration.
4. **Prefill/decode interference.** Colocating compute-bound prefill with bandwidth-bound decode
   causes mutual slowdown; the whole disaggregation line exists to fix it. Agentic loops re-trigger
   prefill constantly, so this is **central to our workload.**
5. **The parallelism axes are orthogonal and compose.** data (ZeRO/FSDP) × tensor (Megatron) ×
   pipeline (GPipe) × sequence/context (Ring) × expert (MoE). Inference is usually TP within a node +
   a placement dimension. Don't equate "model parallelism" with one technique.
6. **MoE serving.** Sparse activation, expert routing, capacity factor, all-to-all comms. Most frontier
   open models you'll serve (DeepSeek, Kimi, Qwen) are MoE; their serving profile differs sharply from
   dense. Know it exists even though it isn't in the tables above.
7. **Multi-head Latent Attention (MLA).** DeepSeek's architectural KV-cache compression — a lever
   distinct from GQA and from quantization. Know it exists.
8. **Structured / constrained decoding** (grammar/FSM, e.g. SGLang's compressed FSM). Agentic
   workloads are JSON/tool-call heavy; constrained decoding is a real serving lever — **and a confound
   for our latency measurements.**
9. **Training-era vs inference-era papers.** Megatron/GPipe/ZeRO are training papers; their parallelism
   ideas transfer to inference but the regimes differ. Cite them for the concept, not as inference benchmarks.
10. **The production stacks are mostly closed.** TensorRT-LLM, FasterTransformer, Triton, NVIDIA Dynamo,
    TGI, llm-d. The "literature" of production is often code, not arXiv. The NVIDIA work lives here —
    and stays out of this repo (IP separation; see [`../06-collab/stakeholders.md`](../06-collab/stakeholders.md)).
11. **Everything is the KV cache.** size (MQA/GQA/MLA), reuse (radix/prefix/prompt cache), eviction
    (H2O/StreamingLLM/KVFlow), precision (KIVI), placement (disaggregation/Mooncake). For agentic
    serving this is THE resource — which is exactly why C1 centers on it.
