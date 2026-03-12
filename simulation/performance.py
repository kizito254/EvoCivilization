from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from .engine import SimulationConfig, run_simulation


@dataclass
class BenchmarkCase:
    agents: int
    ticks: int
    seconds: float
    final_alive: int


@dataclass
class BenchmarkReport:
    seed: int
    phase2: bool
    phase3: bool
    phase5: bool
    cases: List[BenchmarkCase]


def run_scaling_benchmark(
    seed: int = 42,
    scenarios: list[int] | None = None,
    ticks: int = 20,
    enable_phase2: bool = True,
    enable_phase3: bool = True,
    enable_phase5: bool = True,
) -> BenchmarkReport:
    scenarios = scenarios or [1000, 5000, 10000]
    cases: List[BenchmarkCase] = []

    for agents in scenarios:
        config = SimulationConfig(
            seed=seed,
            width=128,
            height=128,
            initial_agents=agents,
            ticks=ticks,
            enable_phase2=enable_phase2,
            enable_phase3=enable_phase3,
            enable_phase5=enable_phase5,
            civilization_count=4,
        )
        start = time.perf_counter()
        result = run_simulation(config)
        elapsed = time.perf_counter() - start
        final_alive = result.metrics[-1].alive_population if result.metrics else 0
        cases.append(BenchmarkCase(agents=agents, ticks=ticks, seconds=elapsed, final_alive=final_alive))

    return BenchmarkReport(
        seed=seed,
        phase2=enable_phase2,
        phase3=enable_phase3,
        phase5=enable_phase5,
        cases=cases,
    )


def write_benchmark_json(report: BenchmarkReport, path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "seed": report.seed,
        "phase2": report.phase2,
        "phase3": report.phase3,
        "phase5": report.phase5,
        "cases": [asdict(c) for c in report.cases],
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out
