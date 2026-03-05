from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Tuple


RESOURCE_TYPES = ("food", "wood", "stone")


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
    inventory: Dict[str, int] = field(default_factory=lambda: {r: 0 for r in RESOURCE_TYPES})


Position = Tuple[int, int]
