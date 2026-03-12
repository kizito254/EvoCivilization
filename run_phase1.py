#!/usr/bin/env python3
from __future__ import annotations

import argparse

from simulation import SimulationConfig, run_simulation, write_metrics_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EvoCivilization simulation (Phase 1/2/3 systems).")
    parser = argparse.ArgumentParser(description="Run EvoCivilization Phase 1 simulation foundation.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--height", type=int, default=64)
    parser.add_argument("--agents", type=int, default=500)
    parser.add_argument("--ticks", type=int, default=100)
    parser.add_argument("--phase2", action="store_true", help="Enable Phase 2 systems: population growth, tech, diplomacy")
    parser.add_argument("--phase3", action="store_true", help="Enable Phase 3 adaptive strategy learning")
    parser.add_argument("--civilizations", type=int, default=3)
    parser.add_argument("--learning-rate", type=float, default=0.2)
    parser.add_argument("--metrics", type=str, default="artifacts/simulation_metrics.csv")
    parser.add_argument("--metrics", type=str, default="artifacts/phase1_metrics.csv")
    args = parser.parse_args()

    config = SimulationConfig(
        seed=args.seed,
        width=args.width,
        height=args.height,
        initial_agents=args.agents,
        ticks=args.ticks,
        enable_phase2=args.phase2 or args.phase3,
        enable_phase3=args.phase3,
        civilization_count=args.civilizations,
        strategy_learning_rate=args.learning_rate,
    )

    result = run_simulation(config)
    out = write_metrics_csv(result, args.metrics)

    final = result.metrics[-1]
    print(
        "Simulation complete: "
        f"tick={final.tick} alive={final.alive_population} deaths={final.deaths} births={final.births} "
        f"avg_tech={final.avg_tech_level:.2f} alliances={final.alliances} wars={final.wars} "
        f"strategy_confidence={final.avg_strategy_confidence:.3f}"
    )
    print(f"Simulation complete: tick={final.tick} alive={final.alive_population} deaths={final.deaths}")
    print(f"Final stockpile: {final.stockpile}")
    print(f"Metrics written: {out}")


if __name__ == "__main__":
    main()
