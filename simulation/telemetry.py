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
                "births",
                "stockpile_food",
                "stockpile_wood",
                "stockpile_stone",
                "civilization_count",
                "avg_tech_level",
                "alliances",
                "wars",
                "avg_strategy_adaptations",
            ]
        )
        for m in result.metrics:
            writer.writerow(
                [
                    m.tick,
                    m.alive_population,
                    m.deaths,
                    m.births,
                    m.stockpile["food"],
                    m.stockpile["wood"],
                    m.stockpile["stone"],
                    m.civilization_count,
                    f"{m.avg_tech_level:.2f}",
                    m.alliances,
                    m.wars,
                    f"{m.avg_strategy_adaptations:.2f}",
                ]
            )

    return out
