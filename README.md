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
AI-driven civilization evolution simulator focused on emergent behavior.

## Vision

EvoCivilization simulates autonomous agents that form settlements, economies, technologies, and geopolitical systems inside a procedurally generated world. Instead of scripted outcomes, macro-history emerges from local decisions.

## Core Pillars

- **Emergent world simulation**: civilization growth from interacting systems.
- **Scalable population simulation**: target 10,000+ autonomous agents.
- **Living History Engine**: convert simulation events into readable historical narrative.
- **Multiple play styles**: Observer, Influencer, and Ruler modes.

## Technology Stack

### Primary runtime
- **Unity** (recommended)
- C# for simulation, AI orchestration, world systems, and UI

### Supporting stack
- Python for ML experiments and offline analysis
- HLSL/ShaderLab for terrain and compute-heavy simulation paths
- SQLite/PostgreSQL for event/history storage
- ML-Agents for reinforcement learning pipelines

## High-Level Architecture

1. **World Generator**
   - Procedural terrain (Perlin/fractal)
   - Biomes, climate, rivers/oceans
   - Resource placement

2. **Civilization Engine**
   - Population, economy, technology, diplomacy, military
   - Territory and relationship modeling

3. **Agent AI System**
   - Needs-driven behavior (food/shelter/security/social)
   - Utility AI + behavior trees (RL optional for strategic adaptation)

4. **Economy Simulation**
   - Production, trade, taxation, logistics
   - Dynamic trade route formation based on comparative surplus/deficit

5. **Technology Progression**
   - Era-based unlocks from primitive to space-age systems
   - Tech unlocks behavior and economic capability changes

6. **Diplomacy + Warfare**
   - Alliances, treaties, trade agreements, conflict
   - Combat outcomes influenced by force, terrain, and technology

7. **Historical Timeline**
   - Records structured events
   - Enables replay, analysis, and narrative generation

## Signature Feature: Living History Engine

The project-defining feature is auto-generated historical storytelling from simulation events.

### Pipeline
1. Event logger records world events (founding, war, migration, disasters, discoveries).
2. Structured history database stores canonical records.
3. Narrative generation layer transforms records into readable history.
4. Documentary mode presents timeline, map replay, and civilization summaries.

### Example event

```json
{
  "year": 420,
  "eventType": "CivilizationFounded",
  "civilization": "Aralon",
  "location": "Northern Plains",
  "population": 1200
}
```

### Example narrative output

> In the year 420, the civilization of Aralon emerged in the northern plains, founded by a coalition of migrating tribes seeking fertile lands.

## Repository Roadmap

### Phase 1 (4–6 weeks): Simulation foundation
- World generation
- Basic agents
- Simple resource economy

### Phase 2 (6–8 weeks): Civilization systems
- Diplomacy
- Technology progression
- Population and city growth

### Phase 3 (8 weeks): AI advancement
- Reinforcement-learning experiments
- Strategic adaptation and policy tuning

### Phase 4 (4 weeks): UX and visualization
- Interactive map
- Statistics dashboard
- Timeline viewer

### Phase 5 (4 weeks): Performance and scale
- DOTS/ECS migration path
- Multithreading and compute shader acceleration
- 10,000+ active agent validation

## Initial Project Structure

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

Phase 2 systems are now integrated into the simulation engine behind `phase2_enabled`:

- **Population growth model** across civilizations (`simulation/civilization.py`).
- **Technology progression** via innovation points and level thresholds (`simulation/civilization.py`).
- **Diplomacy simulation** with dynamic relation drift, alliance/conflict tracking (`simulation/civilization.py`).
- **Extended telemetry** includes civilization population, average technology level, alliances, and conflicts (`simulation/telemetry.py`).

### Run Phase 2

```bash
python3 run_phase2.py --seed 42 --agents 500 --ticks 100 --civilizations 4
```
```

## GitHub Growth Strategy

- Publish simulation clips and GIFs early.
- Keep architecture and dev logs transparent.
- Showcase historical timeline output each milestone.
- Provide reproducible benchmark scenarios.

## Next Steps

- [ ] Bootstrap Unity project skeleton and folder layout.
- [ ] Define simulation tick loop and deterministic seed handling.
- [ ] Implement event schema for the Living History Engine.
- [ ] Add first visualization of timeline replay.
