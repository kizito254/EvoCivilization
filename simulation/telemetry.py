from __future__ import annotations

import csv
from pathlib import Path

from .engine import SimulationResult


def write_metrics_csv(result: SimulationResult, path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "tick",
                "alive_population",
                "deaths",
                "stockpile_food",
                "stockpile_wood",
                "stockpile_stone",
                "civilization_population",
                "avg_technology_level",
                "alliances",
                "conflicts",
            ]
        )
        for m in result.metrics:
            writer.writerow(
                [
                    m.tick,
                    m.alive_population,
                    m.deaths,
                    m.stockpile["food"],
                    m.stockpile["wood"],
                    m.stockpile["stone"],
                    m.civilization_population,
                    round(m.avg_technology_level, 3),
                    m.alliances,
                    m.conflicts,
                ]
            )

    return out
