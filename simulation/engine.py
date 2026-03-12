from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List

from .models import (
    Agent,
    Civilization,
    DiplomaticRelation,
    RESOURCE_TYPES,
    TECH_LEVELS,
)
from .models import Agent, Civilization, DiplomaticRelation, RESOURCE_TYPES, TECH_LEVELS
from .world import World, WorldGenerator

STRATEGIES = ("harvest", "expand", "militarize")

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
    enable_phase2: bool = False
    civilization_count: int = 3
    enable_phase3: bool = False
    strategy_learning_rate: float = 0.2
    phase2_enabled: bool = False
    civilization_count: int = 4


@dataclass
class TickMetrics:
    tick: int
    alive_population: int
    deaths: int
    births: int
    stockpile: Dict[str, int]
    civilization_count: int
    avg_tech_level: float
    alliances: int
    wars: int
    avg_strategy_adaptations: float
    avg_strategy_confidence: float
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
    """Phase 1-3 simulation: economy core + population/tech/diplomacy + adaptive strategy behaviors."""
    """Phase 1+2+3 simulation: economy, population, technology, diplomacy, adaptive strategy behavior."""
    """Phase 1 simulation foundation: world, agents, resource economy, clock, telemetry."""

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.rng = random.Random(config.seed)
        self.world: World = WorldGenerator(seed=config.seed).generate(config.width, config.height)
        self.civilizations = self._create_civilizations(config.civilization_count)
        self.agents: List[Agent] = self._spawn_agents(config.initial_agents)
        self.stockpile: Dict[str, int] = {r: 0 for r in RESOURCE_TYPES}
        self.relations: Dict[tuple[int, int], DiplomaticRelation] = self._init_relations()
        self.strategy_weights: Dict[int, Dict[str, float]] = self._init_strategy_weights()

    def _create_civilizations(self, count: int) -> List[Civilization]:
        return [Civilization(id=i, name=f"Civ-{i+1}") for i in range(max(1, count))]

    def _init_relations(self) -> Dict[tuple[int, int], DiplomaticRelation]:
        rel: Dict[tuple[int, int], DiplomaticRelation] = {}
        for i in range(len(self.civilizations)):
            for j in range(i + 1, len(self.civilizations)):
                rel[(i, j)] = DiplomaticRelation(civ_a=i, civ_b=j)
        return rel

    def _init_strategy_weights(self) -> Dict[int, Dict[str, float]]:
        return {c.id: {"harvest": 1.0, "expand": 1.0, "militarize": 1.0} for c in self.civilizations}
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
            civ_id = idx % len(self.civilizations)
            agents.append(
                Agent(
                    id=idx,
                    x=self.rng.randrange(self.config.width),
                    y=self.rng.randrange(self.config.height),
                    hunger=self.rng.randint(0, 30),
                    civilization_id=civ_id,
                )
            )
        return agents

    def run(self) -> SimulationResult:
        result = SimulationResult(config=self.config)
        for tick in range(1, self.config.ticks + 1):
            deaths = self._step()
            births = 0
            if self.config.enable_phase2:
                births = self._phase2_update(tick)
            if self.config.enable_phase3:
                self._phase3_update(tick)

            alive = sum(1 for a in self.agents if a.alive)
            alliances, wars = self._relation_counts()
            births = self._phase2_update(tick) if (self.config.enable_phase2 or self.config.enable_phase3) else 0
            if self.config.enable_phase3:
                self._phase3_strategy_update()
            alive = sum(1 for a in self.agents if a.alive)
            alliances, wars = self._relation_counts()
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
                    births=births,
                    stockpile=self.stockpile.copy(),
                    civilization_count=len(self.civilizations),
                    avg_tech_level=self._avg_tech_level(),
                    alliances=alliances,
                    wars=wars,
                    avg_strategy_adaptations=self._avg_strategy_adaptations(),
                    avg_strategy_confidence=self._avg_strategy_confidence(),
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
        civ = self.civilizations[agent.civilization_id]

        if self.config.enable_phase3:
            action = self._choose_strategy_action(civ)
            if action == "defend":
                agent.safety = min(100, agent.safety + 2)
                return
            if action == "explore":
                self._move(agent)
                return
        strategy = self._select_strategy(agent.civilization_id)

        if agent.hunger > 55 or strategy == "harvest":
            self._gather(agent, tile, "food", amount=2)
            return

        if strategy == "expand":
            richest = max(RESOURCE_TYPES, key=lambda r: tile.resources.get(r, 0))
            if tile.resources.get(richest, 0) > 0:
                self._gather(agent, tile, richest, amount=2)
                return
            self._move(agent)
            return

        # militarize strategy: lower gather, more positioning (movement)
        if strategy == "militarize" and self.rng.random() < 0.7:
            self._move(agent)
            return


        if agent.hunger > 55:
            self._gather(agent, tile, "food", amount=2)
            return

        richest = max(RESOURCE_TYPES, key=lambda r: tile.resources.get(r, 0))
        if tile.resources.get(richest, 0) > 0:
            self._gather(agent, tile, richest, amount=1)
            return

        self._move(agent)

    def _choose_strategy_action(self, civ: Civilization) -> str:
        roll = self.rng.random()
        if roll < civ.strategy.explore_weight:
            return "explore"
        if roll < civ.strategy.explore_weight + civ.strategy.gather_weight:
            return "gather"
        return "defend"
    def _select_strategy(self, civ_id: int) -> str:
        weights = self.strategy_weights[civ_id]
        total = sum(weights.values())
        pick = self.rng.random() * total
        acc = 0.0
        for name in STRATEGIES:
            acc += weights[name]
            if pick <= acc:
                return name
        return STRATEGIES[-1]

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

    def _phase2_update(self, tick: int) -> int:
        births = 0
        births += self._population_growth(tick)
        self._technology_progression()
        self._diplomacy_update()
        return births

    def _phase3_update(self, tick: int) -> None:
        if tick % 5 != 0:
            return

        civ_alive = self._alive_per_civ()
        for civ in self.civilizations:
            alive = civ_alive.get(civ.id, 0)
            food_reward = min(1.0, self.stockpile["food"] / 2000)
            survival_reward = min(1.0, alive / max(1, self.config.initial_agents // len(self.civilizations)))
            risk_penalty = 0.2 if self._civ_in_war(civ.id) else 0.0
            reward = max(0.0, (0.55 * food_reward + 0.45 * survival_reward) - risk_penalty)

            # lightweight policy-gradient-like update
            civ.strategy.gather_weight += 0.08 * (reward - 0.5)
            civ.strategy.explore_weight += 0.05 * (0.6 - reward)
            civ.strategy.defend_weight += 0.06 * (risk_penalty + 0.2 - reward / 2)
            self._normalize_strategy(civ)
            civ.strategy.adaptations += 1

    def _normalize_strategy(self, civ: Civilization) -> None:
        civ.strategy.explore_weight = max(0.05, min(0.9, civ.strategy.explore_weight))
        civ.strategy.gather_weight = max(0.05, min(0.9, civ.strategy.gather_weight))
        civ.strategy.defend_weight = max(0.05, min(0.9, civ.strategy.defend_weight))
        s = civ.strategy.explore_weight + civ.strategy.gather_weight + civ.strategy.defend_weight
        civ.strategy.explore_weight /= s
        civ.strategy.gather_weight /= s
        civ.strategy.defend_weight /= s

    def _civ_in_war(self, civ_id: int) -> bool:
        for rel in self.relations.values():
            if rel.status != "war":
                continue
            if rel.civ_a == civ_id or rel.civ_b == civ_id:
                return True
        return False

    def _population_growth(self, tick: int) -> int:
        if tick % 10 != 0:
            return 0

        new_agents: List[Agent] = []
        civ_alive = self._alive_per_civ()
        for civ_id, alive in civ_alive.items():
            if alive <= 0:
                continue
            if self.stockpile["food"] < 5:
                continue
            self.stockpile["food"] -= 5

            grow_cost = 4 if self._dominant_strategy(civ_id) == "expand" else 5
            if self.stockpile["food"] < grow_cost:
                continue

            self.stockpile["food"] -= grow_cost
            new_agents.append(
                Agent(
                    id=len(self.agents) + len(new_agents),
                    x=self.rng.randrange(self.config.width),
                    y=self.rng.randrange(self.config.height),
                    hunger=10,
                    civilization_id=civ_id,
                )
            )

        self.agents.extend(new_agents)
        return len(new_agents)

    def _technology_progression(self) -> None:
        civ_alive = self._alive_per_civ()
        for civ in self.civilizations:
            points = civ_alive.get(civ.id, 0) // 25 + self.stockpile["wood"] // 100 + self.stockpile["stone"] // 100
            if self.config.enable_phase3:
                points += int(3 * civ.strategy.gather_weight)
            strategy_bonus = 2 if self._dominant_strategy(civ.id) == "harvest" else 0
            points = (
                civ_alive.get(civ.id, 0) // 25
                + self.stockpile["wood"] // 100
                + self.stockpile["stone"] // 100
                + strategy_bonus
            )
            civ.tech_points += points
            while civ.tech_level_idx < len(TECH_LEVELS) - 1:
                threshold = (civ.tech_level_idx + 1) * 60
                if civ.tech_points < threshold:
                    break
                civ.tech_level_idx += 1

    def _diplomacy_update(self) -> None:
        civ_alive = self._alive_per_civ()
        for rel in self.relations.values():
            a_pop = civ_alive.get(rel.civ_a, 0)
            b_pop = civ_alive.get(rel.civ_b, 0)
            power_delta = (a_pop - b_pop) // 10
            resource_pressure = -2 if self.stockpile["food"] < 100 else 1
            random_drift = self.rng.randint(-2, 2)
            rel.score += power_delta + resource_pressure + random_drift
            rel.score = max(-100, min(100, rel.score))

            stance_delta = 0
            if self._dominant_strategy(rel.civ_a) == "militarize" or self._dominant_strategy(rel.civ_b) == "militarize":
                stance_delta -= 1
            random_drift = self.rng.randint(-2, 2)
            rel.score += power_delta + resource_pressure + stance_delta + random_drift
            rel.score = max(-100, min(100, rel.score))

    def _phase3_strategy_update(self) -> None:
        civ_alive = self._alive_per_civ()
        for civ in self.civilizations:
            reward = self._strategy_reward(civ.id, civ_alive.get(civ.id, 0))
            dominant = self._dominant_strategy(civ.id)
            weights = self.strategy_weights[civ.id]
            lr = self.config.strategy_learning_rate

            weights[dominant] = max(0.1, weights[dominant] + lr * reward)
            # mild exploration decay for non-dominant strategies
            for s in STRATEGIES:
                if s != dominant:
                    weights[s] = max(0.1, weights[s] * (1 - lr * 0.15))

            # keep weights bounded
            for s in STRATEGIES:
                weights[s] = min(6.0, weights[s])

    def _strategy_reward(self, civ_id: int, alive_pop: int) -> float:
        food_signal = self.stockpile["food"] / max(1, alive_pop)
        diplomacy_signal = 0.0
        for rel in self.relations.values():
            if rel.civ_a == civ_id or rel.civ_b == civ_id:
                diplomacy_signal += rel.score / 100
        tech_signal = self.civilizations[civ_id].tech_level_idx * 0.2
        return max(-2.0, min(2.0, (food_signal * 0.1) + diplomacy_signal + tech_signal))

    def _dominant_strategy(self, civ_id: int) -> str:
        weights = self.strategy_weights[civ_id]
        return max(STRATEGIES, key=lambda s: weights[s])

    def _alive_per_civ(self) -> Dict[int, int]:
        counts: Dict[int, int] = {c.id: 0 for c in self.civilizations}
        for agent in self.agents:
            if agent.alive:
                counts[agent.civilization_id] = counts.get(agent.civilization_id, 0) + 1
        return counts

    def _avg_tech_level(self) -> float:
        if not self.civilizations:
            return 0.0
        return sum(c.tech_level_idx for c in self.civilizations) / len(self.civilizations)

    def _avg_strategy_adaptations(self) -> float:
        if not self.civilizations:
            return 0.0
        return sum(c.strategy.adaptations for c in self.civilizations) / len(self.civilizations)

    def _relation_counts(self) -> tuple[int, int]:
        alliances = sum(1 for rel in self.relations.values() if rel.status == "alliance")
        wars = sum(1 for rel in self.relations.values() if rel.status == "war")
        return alliances, wars

    def _avg_strategy_confidence(self) -> float:
        if not self.strategy_weights:
            return 0.0
        conf = []
        for weights in self.strategy_weights.values():
            total = sum(weights.values())
            if total <= 0:
                conf.append(0.0)
                continue
            dominant = max(weights.values()) / total
            conf.append(dominant)
        return sum(conf) / len(conf)


def run_simulation(config: SimulationConfig) -> SimulationResult:
    return Simulation(config).run()
