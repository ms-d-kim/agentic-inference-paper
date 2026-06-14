"""
trace_schema.py — the measurement contract for the agentic-serving pilot.

This is the *shared interface* between the two roles:
  - Serving-internal fields (prefix_cache_hit_tokens, kv_blocks_evicted, gpu_busy_ms, ...)
    are populated by the engine instrumentation. [OWNER: Vinita — vLLM/SGLang internals]
  - Workload/outcome fields (task success, iteration index, available reuse, cost) are
    populated by the benchmark harness + offline analysis. [OWNER: Minseok]

Format target: one OpenTelemetry-style span per model call and per tool call, rolled up
into a per-task record. Keep this stable; everything downstream (analysis, the released
trace) depends on it.

NOTHING here computes serving internals — it only *defines the fields*. The actual cache
counters / eviction hooks are a co-design item for the pilot-design review.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
import json


class Tenancy(str, Enum):
    """Which traffic class produced this request, for multi-tenant interleaving studies."""
    CHAT = "chat"      # baseline chat trace (Azure LLM Inference / BurstGPT)
    AGENT = "agent"    # agentic benchmark request


class Phase(str, Enum):
    """Trajectory phase, per the read/explore -> execute/write structure (2605.26297).
    Annotated post-hoc; leave UNKNOWN if not labeled."""
    READ = "read_explore"
    WRITE = "execute_write"
    UNKNOWN = "unknown"


@dataclass
class ModelCallSpan:
    """One LLM invocation inside an agent trajectory (or a chat turn)."""
    request_id: str
    task_id: str
    iteration_index: int            # which step of the agent loop (0 for chat)
    tenancy: Tenancy
    model: str
    serving_config_id: str          # FK into the experiment matrix cell

    # latency
    ttft_ms: float
    tpot_ms: float
    total_latency_ms: float

    # tokens
    input_tokens: int
    output_tokens: int

    # --- serving internals [OWNER: Vinita] ---
    # The realized-vs-available gap lives here. Populate from engine metrics endpoints.
    prefix_cache_hit_tokens: Optional[int] = None      # realized reuse this call
    prefix_cache_hit_rate: Optional[float] = None      # realized, online, bounded cache
    kv_blocks_allocated: Optional[int] = None
    kv_blocks_evicted: Optional[int] = None            # eviction pressure signal
    gpu_busy_ms: Optional[float] = None
    queue_wait_ms: Optional[float] = None

    phase: Phase = Phase.UNKNOWN


@dataclass
class ToolCallSpan:
    """One tool execution; the source of 'tool-call gaps' (tool wall-time — not necessarily
    GPU-idle under mixed tenancy; see open issue 6 in the pilot README)."""
    request_id: str
    task_id: str
    iteration_index: int
    tool_name: str
    dispatched_at_ms: float
    returned_at_ms: float

    @property
    def tool_gap_ms(self) -> float:
        return self.returned_at_ms - self.dispatched_at_ms


@dataclass
class TaskRecord:
    """Rollup for one benchmark scenario (one task instance)."""
    task_id: str
    benchmark: str                  # e.g. "tau2_bench", "swebench_verified"
    methodology: str                # e.g. "react"
    serving_config_id: str
    success: bool                   # FAIL_TO_PASS / task-defined verification
    n_iterations: int
    e2e_latency_ms: float
    gpu_seconds: float
    total_cost_usd: float

    # --- available reuse, computed OFFLINE [OWNER: Minseok] ---
    # Replay the trace against an *infinite* cache to get the upper bound, then compare
    # to the realized hit rate from ModelCallSpan. The delta is the 'locality tax'.
    reusable_tokens_infinite_cache: Optional[int] = None
    realized_reused_tokens: Optional[int] = None

    model_calls: list[ModelCallSpan] = field(default_factory=list)
    tool_calls: list[ToolCallSpan] = field(default_factory=list)

    # ---- derived metrics (the paper's headline quantities) ----
    @property
    def cost_per_verified_iteration(self) -> Optional[float]:
        """The 'Cost of Grit' unit. None if the task failed (no verified outcome)."""
        if not self.success or self.n_iterations == 0:
            return None
        return self.total_cost_usd / self.n_iterations

    @property
    def locality_gap(self) -> Optional[float]:
        """available - realized reuse, in [0,1]. The core locality-gap quantity.
        NOTE: definition under revision — see open issue 1 in the pilot README
        (must use a common eligible-token denominator and clamp to [0,1])."""
        if self.reusable_tokens_infinite_cache and self.realized_reused_tokens is not None:
            total = self.reusable_tokens_infinite_cache
            if total == 0:
                return None
            available = 1.0
            realized = self.realized_reused_tokens / total
            return available - realized
        return None

    @property
    def total_tool_gap_ms(self) -> float:
        return sum(t.tool_gap_ms for t in self.tool_calls)

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str, indent=2)


if __name__ == "__main__":
    # smoke test
    t = TaskRecord(
        task_id="tau2_0001", benchmark="tau2_bench", methodology="react",
        serving_config_id="react|tau2|mixed0.5|ttl", success=True, n_iterations=12,
        e2e_latency_ms=48230.0, gpu_seconds=31.4, total_cost_usd=0.42,
        reusable_tokens_infinite_cache=100000, realized_reused_tokens=41000,
    )
    print("cost/verified-iter:", t.cost_per_verified_iteration)
    print("locality_gap:", t.locality_gap)
