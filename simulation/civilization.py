from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Civilization:
    id: int
    name: str
    population: int
    technology_level: int = 0
    innovation_points: float = 0.0
    relations: Dict[int, int] = field(default_factory=dict)


@dataclass
class DiplomacySnapshot:
    alliances: int
    conflicts: int


class CivilizationManager:
    """Phase 2 systems: population growth, technology progression, and diplomacy state."""

    def __init__(self, seed: int, civilization_count: int, initial_population: int) -> None:
        self.rng = random.Random(seed + 991)
        self.civilizations = self._create_civilizations(civilization_count, initial_population)

    def _create_civilizations(self, civilization_count: int, initial_population: int) -> List[Civilization]:
        civs: List[Civilization] = []
        base_names = ["Aralon", "Lythia", "Vorin", "Kesh", "Orren", "Myra", "Davos", "Neris"]

        for idx in range(civilization_count):
            pop = max(10, initial_population // civilization_count)
            civs.append(Civilization(id=idx, name=base_names[idx % len(base_names)], population=pop))

        for civ in civs:
            for other in civs:
                if civ.id == other.id:
                    continue
                civ.relations[other.id] = self.rng.randint(-20, 20)

        return civs

    def update(self, stockpile_food: int, alive_agents: int, deaths: int) -> DiplomacySnapshot:
        self._update_population(stockpile_food, alive_agents, deaths)
        self._update_technology(stockpile_food)
        return self._update_diplomacy()

    def _update_population(self, stockpile_food: int, alive_agents: int, deaths: int) -> None:
        total_pop = max(1, sum(c.population for c in self.civilizations))
        food_per_capita = stockpile_food / total_pop

        for civ in self.civilizations:
            # growth when food is abundant, decline under scarcity and deaths pressure.
            growth_rate = 0.006 if food_per_capita > 0.6 else -0.008
            death_pressure = deaths / max(1, alive_agents)
            growth_modifier = growth_rate - death_pressure * 0.8
            delta = int(civ.population * growth_modifier)
            civ.population = max(1, civ.population + delta)

    def _update_technology(self, stockpile_food: int) -> None:
        for civ in self.civilizations:
            civ.innovation_points += 0.3 + (civ.population / 1000.0) + (stockpile_food / 50000.0)
            threshold = 5 + (civ.technology_level * 2)
            if civ.innovation_points >= threshold:
                civ.technology_level += 1
                civ.innovation_points -= threshold

    def _update_diplomacy(self) -> DiplomacySnapshot:
        alliances = 0
        conflicts = 0
        seen_pairs: set[tuple[int, int]] = set()

        for civ in self.civilizations:
            for other_id, score in list(civ.relations.items()):
                drift = self.rng.randint(-3, 3)
                new_score = max(-100, min(100, score + drift))
                civ.relations[other_id] = new_score

                pair = tuple(sorted((civ.id, other_id)))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                if new_score >= 45:
                    alliances += 1
                elif new_score <= -45:
                    conflicts += 1

        return DiplomacySnapshot(alliances=alliances, conflicts=conflicts)

    @property
    def average_technology_level(self) -> float:
        if not self.civilizations:
            return 0.0
        return sum(c.technology_level for c in self.civilizations) / len(self.civilizations)

    @property
    def total_population(self) -> int:
        return sum(c.population for c in self.civilizations)
