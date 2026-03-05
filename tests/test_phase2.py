from __future__ import annotations

import unittest

from simulation import SimulationConfig, run_simulation


class Phase2SimulationTests(unittest.TestCase):
    def test_phase2_metrics_are_populated(self) -> None:
        config = SimulationConfig(
            seed=11,
            width=48,
            height=48,
            initial_agents=500,
            ticks=30,
            phase2_enabled=True,
            civilization_count=4,
        )
        result = run_simulation(config)
        final = result.metrics[-1]

        self.assertGreater(final.civilization_population, 0)
        self.assertGreaterEqual(final.avg_technology_level, 0.0)
        self.assertGreaterEqual(final.alliances, 0)
        self.assertGreaterEqual(final.conflicts, 0)

    def test_phase2_is_deterministic(self) -> None:
        config = SimulationConfig(
            seed=99,
            width=40,
            height=40,
            initial_agents=350,
            ticks=35,
            phase2_enabled=True,
            civilization_count=5,
        )
        r1 = run_simulation(config)
        r2 = run_simulation(config)

        for m1, m2 in zip(r1.metrics, r2.metrics):
            self.assertEqual(m1.civilization_population, m2.civilization_population)
            self.assertEqual(m1.avg_technology_level, m2.avg_technology_level)
            self.assertEqual(m1.alliances, m2.alliances)
            self.assertEqual(m1.conflicts, m2.conflicts)


if __name__ == "__main__":
    unittest.main()
