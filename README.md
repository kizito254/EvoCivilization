# EvoCivilization

AI-Driven Civilization Evolution Simulator where autonomous agents form societies, build economies, develop technologies, and compete in a procedurally generated world.

## Vision

EvoCivilization is designed around **emergent behavior**: world history should arise from interacting systems rather than scripted events.

## Core Pillars

- Procedurally generated worlds with climate/resource dynamics.
- Autonomous agents with needs-driven behavior.
- Civilization-scale systems (economy, diplomacy, warfare, technology).
- Historical timeline and replay.
- Narrative “Living Documentary Mode” that converts events into readable world history.

## Recommended Tech Stack

- **Engine:** Unity (primary), Unreal (alternative)
- **Primary language:** C#
- **Secondary:** Python (ML experimentation), HLSL/ShaderLab (rendering + compute)
- **AI/Simulation:** ML-Agents, behavior trees, utility AI, RL
- **Data:** SQLite/PostgreSQL
- **Version control:** GitHub

## System Architecture

1. **World Generator**
   - Terrain/climate/rivers/resources from Perlin, Voronoi, fractal techniques.
2. **Civilization Engine**
   - Population, economy, culture, technology, military, diplomacy.
3. **Agent AI**
   - Needs: food, shelter, security, social connection.
   - Behaviors: farm/hunt/trade/fight/migrate.
4. **Economy**
   - Production, trade routes, taxation, industry.
5. **Technology Tree**
   - Primitive → Agricultural → Kingdom → Industrial → Space.
6. **Diplomacy**
   - Alliances, trade agreements, conflicts, cultural exchange.
7. **War Simulation**
   - Conflict outcomes based on force, tech, and terrain.
8. **Historical Timeline**
   - Replayable record of world events.

See full details in [`docs/TECHNICAL_BLUEPRINT.md`](docs/TECHNICAL_BLUEPRINT.md).

## Signature Feature: Living Documentary Mode

The standout feature is an **AI-Generated Civilization History** pipeline:

- Event logger records important simulation events.
- Timeline database stores structured history.
- Narrative generator converts events into readable historical entries.
- Documentary UI enables replay, map overlays, and world-history summaries.

See [`docs/LIVING_HISTORY_ENGINE.md`](docs/LIVING_HISTORY_ENGINE.md).

## Development Roadmap

- **Phase 1 (4–6 weeks): Simulation foundation**
  - world generation
  - basic agents
  - simple resource economy
- **Phase 2 (6–8 weeks):** diplomacy, technology, population growth.
- **Phase 3 (8 weeks):** RL-based strategic behavior.
- **Phase 4 (4 weeks):** interactive map + statistics dashboard.
- **Phase 5 (4 weeks):** GPU optimization + large populations.

### Phase 1 Deliverables (Definition of Done)

By the end of Phase 1, the repository should include:

1. **World generation prototype**
   - Deterministic seeded map creation.
   - Biomes + base resource spawning.
2. **Basic autonomous agents**
   - Needs loop (at minimum hunger + safety).
   - Core actions: move, gather, consume, idle.
3. **Simple resource economy**
   - Local stockpile accounting for Food/Wood/Stone.
   - Basic gather-and-consume production loop.
4. **Simulation clock + telemetry**
   - Tick-based update loop.
   - Logged per-tick metrics (population, resources, deaths).

## Proposed Repository Layout

```text
EvoCivilization/
  Assets/
    Scripts/
    AI/
    Terrain/
    UI/
  Simulation/
    Economy/
    Diplomacy/
    Warfare/
  WorldGeneration/
    Terrain/
    Climate/
  Data/
    Civilizations/
    Resources/
  docs/
```

## Performance Target

- Simulate **10,000+ concurrent agents** using multithreading, DOTS/ECS patterns, and compute shaders.

## GitHub Growth Strategy

- Publish simulation videos + GIFs.
- Keep active development logs.
- Maintain architecture and research documentation.
- Showcase generated world histories and replays.

## Next Steps

1. Bootstrap Unity project structure.
2. Implement deterministic simulation clock.
3. Build event schema + timeline store.
4. Deliver first vertical slice:
   - world generation
   - agent survival loop
   - event logging + basic narrative output.

## Phase 1 Implementation (Current)

Implemented in Python as a deterministic simulation scaffold:

- Seeded world generation with biome/resource tiles (`simulation/world.py`).
- Basic autonomous agents with needs-driven actions (`simulation/engine.py`).
- Simple resource economy for Food/Wood/Stone using gather/consume loops (`simulation/engine.py`).
- Tick-based simulation clock and CSV telemetry export (`simulation/engine.py`, `simulation/telemetry.py`).

### Run

```bash
python3 run_phase1.py --seed 42 --agents 500 --ticks 100
```

This writes metrics to `artifacts/phase1_metrics.csv` by default.

## Phase 2 Implementation (Current)

Added an optional Phase 2 scaffold (enabled with `--phase2`) that includes:

- **Population growth:** periodic births per civilization when food supports expansion.
- **Technology progression:** civilization tech points and era advancement based on population/resources.
- **Diplomacy:** pairwise relation scores that evolve into neutral/alliance/war states.

### Run with Phase 2

```bash
python3 run_phase1.py --phase2 --civilizations 3 --agents 500 --ticks 80
```

## Phase 3 Implementation (Current)

Added an optional Phase 3 adaptive strategy layer (enabled with `--phase3`) that includes:

- **Adaptive strategy profiles per civilization** (explore/gather/defend weights).
- **Learning-style updates** every few ticks based on food pressure, survival, and war risk.
- **Strategy telemetry** via `avg_strategy_adaptations` in per-tick metrics.

### Run with Phase 3

```bash
python3 run_phase1.py --phase3 --civilizations 4 --agents 500 --ticks 80
```

## Phase 4 Implementation (Current)

Added an optional Phase 4 visualization layer (enabled with `--phase4`) that includes:

- **Interactive map snapshot** rendered as ASCII terrain/agent overlay.
- **Statistics dashboard** exported as a standalone HTML report.
- **Timeline table** for per-tick simulation metrics (population, resources, diplomacy, strategy adaptation).

### Run with Phase 4

```bash
python3 run_phase1.py --phase4 --phase3 --civilizations 4 --agents 500 --ticks 80
```

## Phase 5 Implementation (Current)

Added an optional Phase 5 performance layer that includes:

- **Optimized tick path** (`--phase5`) that iterates only live-agent indices.
- **High population mode** (`--high-pop`) to trade some fidelity for large-scale throughput.
- **Per-tick performance telemetry** (`step_time_ms`, `effective_agent_updates`).
- **Scaling benchmark utility** (`--benchmark`) for 1k/5k/10k+ population runs.

### Run with Phase 5

```bash
python3 run_phase1.py --phase5 --high-pop --phase3 --agents 10000 --ticks 20 --civilizations 4
```

### Run benchmark

```bash
python3 run_phase1.py --benchmark --ticks 20 --benchmark-counts 1000,5000,10000
```
