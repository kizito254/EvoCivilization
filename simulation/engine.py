from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List

from .civilization import CivilizationManager
from .models import Agent, RESOURCE_TYPES
from .world import World, WorldGenerator


@dataclass
class SimulationConfig:
    seed: int = 42
    width: int = 64
    height: int = 64
    initial_agents: int = 500
    ticks: int = 100
    phase2_enabled: bool = False
    civilization_count: int = 4


@dataclass
class TickMetrics:
    tick: int
    alive_population: int
    deaths: int
    stockpile: Dict[str, int]
    civilization_population: int = 0
    avg_technology_level: float = 0.0
    alliances: int = 0
    conflicts: int = 0


@dataclass
class SimulationResult:
    config: SimulationConfig
    metrics: List[TickMetrics] = field(default_factory=list)


class Simulation:
    """Phase 1 simulation foundation: world, agents, resource economy, clock, telemetry."""

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.rng = random.Random(config.seed)
        self.world: World = WorldGenerator(seed=config.seed).generate(config.width, config.height)
        self.agents: List[Agent] = self._spawn_agents(config.initial_agents)
        self.stockpile: Dict[str, int] = {r: 0 for r in RESOURCE_TYPES}
        self.civilizations = CivilizationManager(
            seed=config.seed,
            civilization_count=config.civilization_count,
            initial_population=config.initial_agents,
        ) if config.phase2_enabled else None

    def _spawn_agents(self, count: int) -> List[Agent]:
        agents: List[Agent] = []
        for idx in range(count):
            agents.append(
                Agent(
                    id=idx,
                    x=self.rng.randrange(self.config.width),
                    y=self.rng.randrange(self.config.height),
                    hunger=self.rng.randint(0, 30),
                )
            )
        return agents

    def run(self) -> SimulationResult:
        result = SimulationResult(config=self.config)
        for tick in range(1, self.config.ticks + 1):
            deaths = self._step()
            alive = sum(1 for a in self.agents if a.alive)
            alliances = 0
            conflicts = 0
            civilization_population = 0
            avg_technology_level = 0.0

            if self.civilizations is not None:
                snapshot = self.civilizations.update(
                    stockpile_food=self.stockpile["food"],
                    alive_agents=alive,
                    deaths=deaths,
                )
                alliances = snapshot.alliances
                conflicts = snapshot.conflicts
                civilization_population = self.civilizations.total_population
                avg_technology_level = self.civilizations.average_technology_level

            result.metrics.append(
                TickMetrics(
                    tick=tick,
                    alive_population=alive,
                    deaths=deaths,
                    stockpile=self.stockpile.copy(),
                    civilization_population=civilization_population,
                    avg_technology_level=avg_technology_level,
                    alliances=alliances,
                    conflicts=conflicts,
                )
            )
        return result

    def _step(self) -> int:
        deaths = 0
        for agent in self.agents:
            if not agent.alive:
                continue

            agent.hunger += 5
            agent.safety = max(0, agent.safety - self.rng.randint(0, 2))

            if agent.hunger >= 90:
                self._consume_or_die(agent)
                if not agent.alive:
                    deaths += 1
                    continue

            self._act(agent)

        return deaths

    def _consume_or_die(self, agent: Agent) -> None:
        if self.stockpile["food"] > 0:
            self.stockpile["food"] -= 1
            agent.hunger = max(0, agent.hunger - 45)
            return

        # fallback from inventory
        if agent.inventory["food"] > 0:
            agent.inventory["food"] -= 1
            agent.hunger = max(0, agent.hunger - 40)
            return

        agent.alive = False

    def _act(self, agent: Agent) -> None:
        tile = self.world.tile_at(agent.x, agent.y)

        if agent.hunger > 55:
            self._gather(agent, tile, "food", amount=2)
            return

        richest = max(RESOURCE_TYPES, key=lambda r: tile.resources.get(r, 0))
        if tile.resources.get(richest, 0) > 0:
            self._gather(agent, tile, richest, amount=1)
            return

        self._move(agent)

    def _gather(self, agent: Agent, tile, resource: str, amount: int) -> None:
        available = tile.resources.get(resource, 0)
        take = min(amount, available)
        if take <= 0:
            self._move(agent)
            return

        tile.resources[resource] -= take
        self.stockpile[resource] += take
        if resource == "food":
            agent.hunger = max(0, agent.hunger - 15 * take)

    def _move(self, agent: Agent) -> None:
        dx, dy = self.rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)))
        agent.x = (agent.x + dx) % self.config.width
        agent.y = (agent.y + dy) % self.config.height


def run_simulation(config: SimulationConfig) -> SimulationResult:
    return Simulation(config).run()
