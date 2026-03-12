from __future__ import annotations

import csv
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .engine import Simulation, SimulationConfig


@dataclass
class BenchmarkRow:
    agents: int
    ticks: int
    duration_s: float
    updates_per_s: float
    final_alive: int


def run_scaling_benchmark(
    agent_counts: Iterable[int],
    ticks: int = 30,
    seed: int = 42,
    width: int = 128,
    height: int = 128,
    civilizations: int = 4,
) -> List[BenchmarkRow]:
    rows: List[BenchmarkRow] = []
    for agents in agent_counts:
        cfg = SimulationConfig(
            seed=seed,
            width=width,
            height=height,
            initial_agents=agents,
            ticks=ticks,
            enable_phase2=True,
            enable_phase3=True,
            enable_phase5=True,
            high_population_mode=True,
            civilization_count=civilizations,
        )
        sim = Simulation(cfg)
        t0 = time.perf_counter()
        result = sim.run()
        elapsed = max(1e-9, time.perf_counter() - t0)
        updates = agents * ticks
        rows.append(
            BenchmarkRow(
                agents=agents,
                ticks=ticks,
                duration_s=elapsed,
                updates_per_s=updates / elapsed,
                final_alive=result.metrics[-1].alive_population if result.metrics else 0,
            )
        )
    return rows


def write_benchmark_csv(rows: List[BenchmarkRow], output_path: str | Path) -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["agents", "ticks", "duration_s", "updates_per_s", "final_alive"])
        for r in rows:
            writer.writerow([r.agents, r.ticks, f"{r.duration_s:.4f}", f"{r.updates_per_s:.2f}", r.final_alive])
    return out
