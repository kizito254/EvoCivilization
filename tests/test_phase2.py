from __future__ import annotations

import unittest

from simulation import SimulationConfig, run_simulation


class Phase2SimulationTests(unittest.TestCase):
    def test_phase2_generates_population_growth(self) -> None:
        config = SimulationConfig(seed=5, width=48, height=48, initial_agents=300, ticks=30, enable_phase2=True)
        result = run_simulation(config)

        total_births = sum(m.births for m in result.metrics)
        self.assertGreater(total_births, 0)

    def test_phase2_technology_progresses(self) -> None:
        config = SimulationConfig(seed=8, width=64, height=64, initial_agents=450, ticks=60, enable_phase2=True)
        result = run_simulation(config)

        self.assertGreaterEqual(result.metrics[-1].avg_tech_level, 1.0)

    def test_phase2_diplomacy_has_non_neutral_outcomes(self) -> None:
        config = SimulationConfig(seed=11, width=64, height=64, initial_agents=500, ticks=80, enable_phase2=True)
        result = run_simulation(config)

        seen = any((m.alliances + m.wars) > 0 for m in result.metrics)
        self.assertTrue(seen)


if __name__ == "__main__":
    unittest.main()
