#!/usr/bin/env python3
from __future__ import annotations

import argparse

from simulation import SimulationConfig, run_simulation, write_metrics_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EvoCivilization Phase 1 simulation foundation.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--height", type=int, default=64)
    parser.add_argument("--agents", type=int, default=500)
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--metrics", type=str, default="artifacts/phase1_metrics.csv")
    args = parser.parse_args()

    config = SimulationConfig(
        seed=args.seed,
        width=args.width,
        height=args.height,
        initial_agents=args.agents,
        ticks=args.ticks,
    )

    result = run_simulation(config)
    out = write_metrics_csv(result, args.metrics)

    final = result.metrics[-1]
    print(f"Simulation complete: tick={final.tick} alive={final.alive_population} deaths={final.deaths}")
    print(f"Final stockpile: {final.stockpile}")
    print(f"Metrics written: {out}")


if __name__ == "__main__":
    main()
