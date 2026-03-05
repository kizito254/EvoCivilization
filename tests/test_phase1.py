from __future__ import annotations

import csv
import tempfile
import unittest

from simulation import SimulationConfig, run_simulation, write_metrics_csv


class Phase1SimulationTests(unittest.TestCase):
    def test_deterministic_seed_reproduces_metrics(self) -> None:
        config = SimulationConfig(seed=7, width=32, height=32, initial_agents=120, ticks=40)
        r1 = run_simulation(config)
        r2 = run_simulation(config)

        self.assertEqual(len(r1.metrics), len(r2.metrics))
        for m1, m2 in zip(r1.metrics, r2.metrics):
            self.assertEqual(m1.alive_population, m2.alive_population)
            self.assertEqual(m1.deaths, m2.deaths)
            self.assertEqual(m1.stockpile, m2.stockpile)

    def test_500_agents_runs_and_records_metrics(self) -> None:
        config = SimulationConfig(seed=42, width=64, height=64, initial_agents=500, ticks=25)
        result = run_simulation(config)

        self.assertEqual(len(result.metrics), 25)
        self.assertGreaterEqual(result.metrics[0].alive_population, result.metrics[-1].alive_population)
        self.assertIn("food", result.metrics[-1].stockpile)
        self.assertIn("wood", result.metrics[-1].stockpile)
        self.assertIn("stone", result.metrics[-1].stockpile)

    def test_metrics_csv_export(self) -> None:
        config = SimulationConfig(seed=9, width=20, height=20, initial_agents=80, ticks=10)
        result = run_simulation(config)

        with tempfile.TemporaryDirectory() as tmp:
            path = write_metrics_csv(result, f"{tmp}/metrics.csv")
            with path.open("r", encoding="utf-8") as f:
                rows = list(csv.reader(f))

        self.assertEqual(rows[0][0], "tick")
        self.assertEqual(len(rows), 11)  # header + 10 ticks


if __name__ == "__main__":
    unittest.main()
