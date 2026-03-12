from __future__ import annotations

import tempfile
import unittest

from simulation import Simulation, SimulationConfig, run_scaling_benchmark, write_benchmark_csv


class Phase5PerformanceTests(unittest.TestCase):
    def test_phase5_high_population_mode_runs(self) -> None:
        sim = Simulation(
            SimulationConfig(
                seed=33,
                width=128,
                height=128,
                initial_agents=10000,
                ticks=8,
                enable_phase2=True,
                enable_phase3=True,
                enable_phase5=True,
                high_population_mode=True,
                civilization_count=4,
            )
        )
        result = sim.run()
        self.assertEqual(len(result.metrics), 8)
        self.assertGreater(result.metrics[-1].alive_population, 0)
        self.assertGreater(result.metrics[-1].effective_agent_updates, 0)

    def test_phase5_benchmark_export(self) -> None:
        rows = run_scaling_benchmark([500, 1000], ticks=5, seed=34)
        self.assertEqual(len(rows), 2)
        self.assertGreater(rows[0].updates_per_s, 0)

        with tempfile.TemporaryDirectory() as tmp:
            out = write_benchmark_csv(rows, f"{tmp}/bench.csv")
            data = out.read_text(encoding="utf-8")

        self.assertIn("agents,ticks,duration_s,updates_per_s,final_alive", data)


if __name__ == "__main__":
    unittest.main()
