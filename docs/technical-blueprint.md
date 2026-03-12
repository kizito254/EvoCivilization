# EvoCivilization Technical Blueprint

This document translates the high-level concept into an implementation-oriented plan.

## 1) Module Boundaries

### World
- `WorldSeed` + deterministic PRNG
- Terrain and biome layers
- Climate simulation (temperature, humidity, rainfall)
- Resource map generation

### Simulation Core
- Fixed tick scheduler
- System ordering and dependency graph
- Event bus for inter-system communication

### Agent Layer
- Individual agents with state/needs
- Action selection via utility scoring
- Optional RL policy integration behind feature flags

### Society Layer
- Settlement growth model
- Governance profile and culture vectors
- Internal stability and unrest metrics

### Macro Systems
- Economy: supply, demand, route formation
- Diplomacy: trust matrix, treaties, hostilities
- Warfare: mobilization, battle resolution, attrition
- Technology: prerequisites, diffusion, adoption rates

### History Layer
- Immutable event records
- Compression/indexing for long-run simulations
- Narrative generation and summarization

## 2) Data Design (initial)

### Core entities
- `Agent`
- `Settlement`
- `Civilization`
- `ResourceNode`
- `TradeRoute`
- `War`
- `Technology`
- `HistoricalEvent`

### Event model
Each event should include:
- `event_id`
- `tick` / `year`
- `event_type`
- `participants`
- `location`
- `metrics` (structured key-value payload)
- `tags`

## 3) Living History Engine (implementation)

### Step A: Instrument systems
All major systems emit typed events to a central event pipeline.

### Step B: Persistence
Persist typed events to SQLite for local runs and PostgreSQL for large experiments.

### Step C: Narrative generation
Use deterministic templates first, then optionally augment with LLM-generated prose.

### Step D: Documentary mode
Provide timeline, map overlays, and civilization dossier pages.

## 4) Performance Strategy

- Use fixed timestep simulation.
- Isolate read/write phases per system.
- Batch pathfinding and economy updates.
- Move expensive aggregate calculations to jobs/compute.
- Keep event logging append-only and streamable.

## 5) Milestone Acceptance Criteria

### M1: Sandbox world running
- Deterministic world from seed
- 1,000 agents living/gathering/migrating
- Baseline resource economy loop

### M2: Multi-civilization interactions
- At least 4 civilizations
- Trade and diplomacy events visible on timeline
- Technology unlocks affecting productivity

### M3: Living documentary alpha
- Narrative summaries generated per era
- Replayable timeline and border visualization
- Exportable “world chronicle” markdown report

## 6) Risks and Mitigations

- **Simulation instability** → enforce bounded values and sanity checks.
- **Performance collapse at scale** → profile early; prioritize jobification hotspots.
- **Unreadable event noise** → event taxonomy + aggregation passes.
- **Narrative inconsistency** → canonical data-first narration pipeline.
