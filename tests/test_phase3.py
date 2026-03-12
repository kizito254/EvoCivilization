from __future__ import annotations

import unittest

from simulation import SimulationConfig, run_simulation


class Phase3SimulationTests(unittest.TestCase):
    def test_phase3_adaptation_progresses_over_time(self) -> None:
        config = SimulationConfig(
            seed=21,
            width=64,
            height=64,
            initial_agents=500,
            ticks=50,
            enable_phase2=True,
            enable_phase3=True,
            civilization_count=4,
        )
        result = run_simulation(config)

        self.assertGreater(result.metrics[-1].avg_strategy_adaptations, 0.0)
        self.assertGreater(result.metrics[-1].avg_strategy_adaptations, result.metrics[0].avg_strategy_adaptations)

    def test_phase3_keeps_population_alive(self) -> None:
        config = SimulationConfig(
            seed=22,
            width=64,
            height=64,
            initial_agents=500,
            ticks=80,
            enable_phase2=True,
            enable_phase3=True,
            civilization_count=3,
        )
        result = run_simulation(config)

        self.assertGreater(result.metrics[-1].alive_population, 0)


if __name__ == "__main__":
    unittest.main()
