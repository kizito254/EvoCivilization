from __future__ import annotations

import sqlite3
import tempfile
import unittest

from simulation import (
    Simulation,
    SimulationConfig,
    generate_history_events,
    render_narrative,
    write_history_book,
    write_history_db,
)


class LivingHistoryTests(unittest.TestCase):
    def test_history_events_generated(self) -> None:
        sim = Simulation(
            SimulationConfig(
                seed=51,
                width=64,
                height=64,
                initial_agents=400,
                ticks=30,
                enable_phase2=True,
                enable_phase3=True,
            )
        )
        result = sim.run()
        events = generate_history_events(result, sim.civilizations)

        self.assertGreater(len(events), 0)
        self.assertTrue(any(e.event_type == "CivilizationFounded" for e in events))

    def test_history_db_and_book_exports(self) -> None:
        sim = Simulation(
            SimulationConfig(
                seed=52,
                width=40,
                height=40,
                initial_agents=240,
                ticks=20,
                enable_phase2=True,
            )
        )
        result = sim.run()
        events = generate_history_events(result, sim.civilizations)

        with tempfile.TemporaryDirectory() as tmp:
            db_path = write_history_db(events, f"{tmp}/events.db")
            book_path = write_history_book(events, f"{tmp}/history.md")

            conn = sqlite3.connect(db_path)
            try:
                count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            finally:
                conn.close()

            text = book_path.read_text(encoding="utf-8")

        self.assertEqual(count, len(events))
        self.assertIn("# The Living History", text)
        self.assertGreater(len(render_narrative(events)), 0)


if __name__ == "__main__":
    unittest.main()
