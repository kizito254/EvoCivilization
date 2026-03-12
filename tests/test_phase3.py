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
from simulation import Simulation, SimulationConfig, run_simulation


class Phase3SimulationTests(unittest.TestCase):
    def test_phase3_exposes_strategy_confidence_metric(self) -> None:
        config = SimulationConfig(seed=12, width=64, height=64, initial_agents=500, ticks=50, enable_phase3=True)
        result = run_simulation(config)

        self.assertEqual(len(result.metrics), 50)
        self.assertGreaterEqual(result.metrics[-1].avg_strategy_confidence, 0.34)
        self.assertLessEqual(result.metrics[-1].avg_strategy_confidence, 1.0)

    def test_phase3_adapts_strategy_weights(self) -> None:
        config = SimulationConfig(seed=13, width=48, height=48, initial_agents=300, ticks=40, enable_phase3=True)
        sim = Simulation(config)

        initial = {civ: weights.copy() for civ, weights in sim.strategy_weights.items()}
        sim.run()

        changed = False
        for civ_id, before in initial.items():
            after = sim.strategy_weights[civ_id]
            if any(abs(after[k] - before[k]) > 1e-9 for k in before):
                changed = True
                break
        self.assertTrue(changed)


if __name__ == "__main__":
    unittest.main()
