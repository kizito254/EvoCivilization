#!/usr/bin/env python3
from __future__ import annotations

import argparse

from simulation import (
    Simulation,
    SimulationConfig,
    generate_history_events,
    render_ascii_map,
    run_scaling_benchmark,
    write_benchmark_csv,
    write_dashboard_html,
    write_history_book,
    write_history_db,
    write_metrics_csv,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EvoCivilization simulation (Phase 1 + optional Phase 2/3/4/5 + history systems).")
    parser = argparse.ArgumentParser(description="Run EvoCivilization simulation (Phase 1 + optional Phase 2/3/4/5 systems).")
from simulation import Simulation, SimulationConfig, render_ascii_map, write_dashboard_html, write_metrics_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EvoCivilization simulation (Phase 1 + optional Phase 2/3/4 systems).")
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
    parser.add_argument("--phase3", action="store_true", help="Enable Phase 3 adaptive strategy behavior updates")
    parser.add_argument("--phase4", action="store_true", help="Enable Phase 4 dashboard/map export")
    parser.add_argument("--phase5", action="store_true", help="Enable Phase 5 performance mode optimizations")
    parser.add_argument("--history", action="store_true", help="Enable Living History export (SQLite + markdown)")
    parser.add_argument("--high-pop", action="store_true", help="Enable high-population fidelity tradeoffs")
    parser.add_argument("--benchmark", action="store_true", help="Run Phase 5 scaling benchmark and export CSV")
    parser.add_argument("--benchmark-counts", type=str, default="1000,5000,10000")
    parser.add_argument("--civilizations", type=int, default=3)
    parser.add_argument("--metrics", type=str, default="artifacts/simulation_metrics.csv")
    parser.add_argument("--dashboard", type=str, default="artifacts/phase4_dashboard.html")
    parser.add_argument("--benchmark-out", type=str, default="artifacts/phase5_benchmark.csv")
    parser.add_argument("--history-db", type=str, default="artifacts/history/events.db")
    parser.add_argument("--history-book", type=str, default="artifacts/history/history_book.md")
    args = parser.parse_args()

    if args.benchmark:
        counts = [int(x.strip()) for x in args.benchmark_counts.split(",") if x.strip()]
        rows = run_scaling_benchmark(
            counts,
            ticks=args.ticks,
            seed=args.seed,
            width=max(args.width, 128),
            height=max(args.height, 128),
            civilizations=max(2, args.civilizations),
        )
        out = write_benchmark_csv(rows, args.benchmark_out)
        print(f"Benchmark written: {out}")
        for row in rows:
            print(
                f"agents={row.agents} ticks={row.ticks} duration={row.duration_s:.3f}s "
                f"updates/s={row.updates_per_s:.2f} alive={row.final_alive}"
            )
        return

    parser.add_argument("--civilizations", type=int, default=3)
    parser.add_argument("--metrics", type=str, default="artifacts/simulation_metrics.csv")
    parser.add_argument("--dashboard", type=str, default="artifacts/phase4_dashboard.html")
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
        civilization_count=args.civilizations,
        enable_phase3=args.phase3,
        enable_phase5=args.phase5,
        high_population_mode=args.high_pop,
    )

    simulation = Simulation(config)
    result = simulation.run()
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
        f"strategy_adapt={final.avg_strategy_adaptations:.2f} step_ms={final.step_time_ms:.3f} "
        f"updates={final.effective_agent_updates}"
        f"strategy_adapt={final.avg_strategy_adaptations:.2f}"
    )
    print(f"Final stockpile: {final.stockpile}")
    print(f"Metrics written: {out}")

    if args.phase4:
        ascii_map = render_ascii_map(simulation.world, simulation.agents)
        dashboard_path = write_dashboard_html(result, ascii_map, args.dashboard)
        print(f"Dashboard written: {dashboard_path}")

    if args.history:
        events = generate_history_events(result, simulation.civilizations)
        db_path = write_history_db(events, args.history_db)
        book_path = write_history_book(events, args.history_book)
        print(f"History DB written: {db_path}")
        print(f"History book written: {book_path}")
        f"strategy_confidence={final.avg_strategy_confidence:.3f}"
    )
    print(f"Simulation complete: tick={final.tick} alive={final.alive_population} deaths={final.deaths}")
    print(f"Final stockpile: {final.stockpile}")
    print(f"Metrics written: {out}")


if __name__ == "__main__":
    main()
