#!/usr/bin/env python3
from __future__ import annotations

import argparse

from simulation import SimulationConfig, run_simulation, write_metrics_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EvoCivilization Phase 2 systems (population, technology, diplomacy).")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--height", type=int, default=64)
    parser.add_argument("--agents", type=int, default=500)
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--civilizations", type=int, default=4)
    parser.add_argument("--metrics", type=str, default="artifacts/phase2_metrics.csv")
    args = parser.parse_args()

    config = SimulationConfig(
        seed=args.seed,
        width=args.width,
        height=args.height,
        initial_agents=args.agents,
        ticks=args.ticks,
        phase2_enabled=True,
        civilization_count=args.civilizations,
    )

    result = run_simulation(config)
    out = write_metrics_csv(result, args.metrics)

    final = result.metrics[-1]
    print(f"Phase 2 simulation complete: tick={final.tick} alive={final.alive_population}")
    print(
        "Civilizations -> "
        f"population={final.civilization_population} avg_tech={final.avg_technology_level:.2f} "
        f"alliances={final.alliances} conflicts={final.conflicts}"
    )
    print(f"Metrics written: {out}")


if __name__ == "__main__":
    main()
