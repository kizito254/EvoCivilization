from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .engine import SimulationResult
from .models import Civilization


@dataclass
class HistoryEvent:
    year: int
    event_type: str
    title: str
    details: str


def generate_history_events(result: SimulationResult, civilizations: Iterable[Civilization]) -> List[HistoryEvent]:
    events: List[HistoryEvent] = []
    civs = list(civilizations)

    for civ in civs:
        events.append(
            HistoryEvent(
                year=1,
                event_type="CivilizationFounded",
                title=f"{civ.name} founded",
                details=f"{civ.name} emerged at the dawn of the simulation.",
            )
        )

    prev_alliances = 0
    prev_wars = 0
    prev_avg_tech = 0.0
    for m in result.metrics:
        if m.births > 0:
            events.append(
                HistoryEvent(
                    year=m.tick,
                    event_type="PopulationGrowth",
                    title="Population expansion",
                    details=f"Birth waves added {m.births} new citizens across civilizations.",
                )
            )

        if m.deaths > 0:
            events.append(
                HistoryEvent(
                    year=m.tick,
                    event_type="PopulationDecline",
                    title="Population losses",
                    details=f"{m.deaths} citizens died amid resource pressure.",
                )
            )

        if m.avg_tech_level >= prev_avg_tech + 1.0:
            events.append(
                HistoryEvent(
                    year=m.tick,
                    event_type="TechnologyMilestone",
                    title="Technological milestone reached",
                    details=f"Average civilization technology index reached {m.avg_tech_level:.2f}.",
                )
            )
            prev_avg_tech = m.avg_tech_level

        if m.alliances > prev_alliances:
            events.append(
                HistoryEvent(
                    year=m.tick,
                    event_type="AllianceFormed",
                    title="New alliance formed",
                    details=f"Alliance count increased to {m.alliances}.",
                )
            )
        prev_alliances = m.alliances

        if m.wars > prev_wars:
            events.append(
                HistoryEvent(
                    year=m.tick,
                    event_type="WarStarted",
                    title="Conflict escalated",
                    details=f"War count increased to {m.wars}.",
                )
            )
        prev_wars = m.wars

    return events


def write_history_db(events: List[HistoryEvent], db_path: str | Path) -> Path:
    out = Path(db_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(out)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                title TEXT NOT NULL,
                details TEXT NOT NULL
            )
            """
        )
        cur.execute("DELETE FROM events")
        cur.executemany(
            "INSERT INTO events(year, event_type, title, details) VALUES(?, ?, ?, ?)",
            [(e.year, e.event_type, e.title, e.details) for e in events],
        )
        conn.commit()
    finally:
        conn.close()

    return out


def render_narrative(events: List[HistoryEvent]) -> List[str]:
    lines: List[str] = []
    for e in events:
        if e.event_type == "CivilizationFounded":
            lines.append(f"Year {e.year}: {e.title}. {e.details}")
        elif e.event_type == "TechnologyMilestone":
            lines.append(f"Year {e.year}: Scholars recorded a breakthrough. {e.details}")
        elif e.event_type == "AllianceFormed":
            lines.append(f"Year {e.year}: Diplomats secured a pact. {e.details}")
        elif e.event_type == "WarStarted":
            lines.append(f"Year {e.year}: Tensions erupted into open conflict. {e.details}")
        elif e.event_type == "PopulationGrowth":
            lines.append(f"Year {e.year}: Settlements flourished. {e.details}")
        else:
            lines.append(f"Year {e.year}: {e.title}. {e.details}")
    return lines


def write_history_book(events: List[HistoryEvent], output_path: str | Path, world_name: str = "EvoCivilization") -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# The Living History of {world_name}", "", "## Timeline", ""]
    lines.extend(f"- {line}" for line in render_narrative(events))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
