from __future__ import annotations

import tempfile
import unittest

from simulation import (
    Simulation,
    SimulationConfig,
    render_ascii_map,
    write_dashboard_html,
)


class Phase4VisualizationTests(unittest.TestCase):
    def test_ascii_map_contains_terrain_or_agents(self) -> None:
        sim = Simulation(
            SimulationConfig(seed=3, width=32, height=32, initial_agents=120, ticks=20, enable_phase2=True, enable_phase3=True)
        )
        sim.run()

        ascii_map = render_ascii_map(sim.world, sim.agents, width=24, height=12)
        self.assertEqual(len(ascii_map.splitlines()), 12)
        self.assertTrue(any(ch in ascii_map for ch in ["A", ".", "T", "^", "~", "W"]))

    def test_dashboard_html_written(self) -> None:
        sim = Simulation(
            SimulationConfig(seed=4, width=40, height=40, initial_agents=200, ticks=25, enable_phase2=True, enable_phase3=True)
        )
        result = sim.run()
        ascii_map = render_ascii_map(sim.world, sim.agents)

        with tempfile.TemporaryDirectory() as tmp:
            out = write_dashboard_html(result, ascii_map, f"{tmp}/dashboard.html")
            html = out.read_text(encoding="utf-8")

        self.assertIn("Phase 4", html)
        self.assertIn("Timeline Metrics", html)
        self.assertIn("Interactive Map Snapshot", html)


if __name__ == "__main__":
    unittest.main()
