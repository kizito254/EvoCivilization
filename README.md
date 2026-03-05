# EvoCivilization

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
