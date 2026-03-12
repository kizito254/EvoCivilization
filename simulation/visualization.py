from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from .engine import SimulationResult
from .models import Agent, Biome
from .world import World


BIOME_GLYPHS = {
    Biome.PLAINS: ".",
    Biome.FOREST: "T",
    Biome.HILLS: "^",
    Biome.DESERT: "~",
    Biome.WATER: "W",
}


def render_ascii_map(world: World, agents: Iterable[Agent], width: int = 48, height: int = 24) -> str:
    """Render a compact ASCII map with biome glyphs and live agent overlays."""
    width = max(8, min(width, world.width))
    height = max(8, min(height, world.height))

    alive_positions = {(a.x % world.width, a.y % world.height) for a in agents if a.alive}

    lines: list[str] = []
    for y in range(height):
        row: list[str] = []
        for x in range(width):
            if (x, y) in alive_positions:
                row.append("A")
            else:
                biome = world.tile_at(x, y).biome
                row.append(BIOME_GLYPHS.get(biome, "?"))
        lines.append("".join(row))

    return "\n".join(lines)


def write_dashboard_html(result: SimulationResult, ascii_map: str, output_path: str | Path) -> Path:
    """Write a lightweight HTML dashboard for Phase 4 map + simulation metrics."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    rows = "\n".join(
        f"<tr><td>{m.tick}</td><td>{m.alive_population}</td><td>{m.deaths}</td><td>{m.births}</td>"
        f"<td>{m.stockpile['food']}</td><td>{m.stockpile['wood']}</td><td>{m.stockpile['stone']}</td>"
        f"<td>{m.avg_tech_level:.2f}</td><td>{m.alliances}</td><td>{m.wars}</td>"
        f"<td>{m.avg_strategy_adaptations:.2f}</td></tr>"
        for m in result.metrics
    )

    html = f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>EvoCivilization Phase 4 Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 1rem 2rem; }}
    pre {{ background: #111; color: #9fe6a0; padding: 1rem; overflow: auto; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 0.9rem; }}
    th, td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: right; }}
    th:first-child, td:first-child {{ text-align: left; }}
    .summary {{ display: grid; grid-template-columns: repeat(4, minmax(130px, 1fr)); gap: 0.5rem; margin-bottom: 1rem; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 0.5rem; }}
  </style>
</head>
<body>
  <h1>EvoCivilization — Phase 4 Dashboard</h1>
  <div class='summary'>
    <div class='card'><strong>Ticks</strong><br>{len(result.metrics)}</div>
    <div class='card'><strong>Final Population</strong><br>{result.metrics[-1].alive_population if result.metrics else 0}</div>
    <div class='card'><strong>Final Avg Tech</strong><br>{result.metrics[-1].avg_tech_level if result.metrics else 0:.2f}</div>
    <div class='card'><strong>Final Alliances/Wars</strong><br>{result.metrics[-1].alliances if result.metrics else 0}/{result.metrics[-1].wars if result.metrics else 0}</div>
  </div>

  <h2>Interactive Map Snapshot (ASCII)</h2>
  <pre>{escape(ascii_map)}</pre>

  <h2>Timeline Metrics</h2>
  <table>
    <thead>
      <tr>
        <th>Tick</th><th>Alive</th><th>Deaths</th><th>Births</th><th>Food</th><th>Wood</th><th>Stone</th>
        <th>AvgTech</th><th>Alliances</th><th>Wars</th><th>StrategyAdapt</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>
"""

    out.write_text(html, encoding="utf-8")
    return out
