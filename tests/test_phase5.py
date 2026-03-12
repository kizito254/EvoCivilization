from __future__ import annotations

import json
import tempfile
import unittest

from simulation import (
    SimulationConfig,
    run_scaling_benchmark,
    run_simulation,
    write_benchmark_json,
)


class Phase5PerformanceTests(unittest.TestCase):
    def test_phase5_runs_10000_agents(self) -> None:
        config = SimulationConfig(
            seed=33,
            width=128,
            height=128,
            initial_agents=10000,
            ticks=8,
            enable_phase2=True,
            enable_phase3=True,
            enable_phase5=True,
            civilization_count=4,
        )
        result = run_simulation(config)

        self.assertEqual(len(result.metrics), 8)
        self.assertGreater(result.metrics[-1].alive_population, 0)

    def test_phase5_benchmark_report_write(self) -> None:
        report = run_scaling_benchmark(seed=34, scenarios=[1000, 2000], ticks=5)

        with tempfile.TemporaryDirectory() as tmp:
            path = write_benchmark_json(report, f"{tmp}/bench.json")
            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(len(payload["cases"]), 2)
        self.assertIn("seconds", payload["cases"][0])


if __name__ == "__main__":
    unittest.main()
