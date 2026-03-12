from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Tuple


RESOURCE_TYPES = ("food", "wood", "stone")
TECH_LEVELS = ("primitive", "agricultural", "kingdom", "industrial", "space")


class Biome(str, Enum):
    PLAINS = "plains"
    FOREST = "forest"
    HILLS = "hills"
    DESERT = "desert"
    WATER = "water"


@dataclass
class Tile:
    biome: Biome
    resources: Dict[str, int] = field(default_factory=dict)


@dataclass
class Agent:
    id: int
    x: int
    y: int
    hunger: int = 0
    safety: int = 100
    alive: bool = True
    civilization_id: int = 0
    inventory: Dict[str, int] = field(default_factory=lambda: {r: 0 for r in RESOURCE_TYPES})


@dataclass
class StrategyProfile:
    explore_weight: float = 0.34
    gather_weight: float = 0.33
    defend_weight: float = 0.33
    adaptations: int = 0


@dataclass
class Civilization:
    id: int
    name: str
    tech_points: int = 0
    tech_level_idx: int = 0
    strategy: StrategyProfile = field(default_factory=StrategyProfile)

    @property
    def tech_level(self) -> str:
        return TECH_LEVELS[self.tech_level_idx]


@dataclass
class DiplomaticRelation:
    civ_a: int
    civ_b: int
    score: int = 0

    @property
    def status(self) -> str:
        if self.score >= 35:
            return "alliance"
        if self.score <= -35:
            return "war"
        return "neutral"


    inventory: Dict[str, int] = field(default_factory=lambda: {r: 0 for r in RESOURCE_TYPES})


Position = Tuple[int, int]
