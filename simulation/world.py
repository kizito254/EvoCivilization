from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from .models import Biome, Tile


@dataclass
class World:
    width: int
    height: int
    tiles: List[List[Tile]]

    def tile_at(self, x: int, y: int) -> Tile:
        return self.tiles[y % self.height][x % self.width]


class WorldGenerator:
    """Deterministic seeded world generation with biome + base resource spawning."""

    def __init__(self, seed: int) -> None:
        self._rng = random.Random(seed)

    def generate(self, width: int, height: int) -> World:
        tiles: List[List[Tile]] = []
        for y in range(height):
            row: List[Tile] = []
            for x in range(width):
                biome = self._choose_biome(x, y)
                row.append(Tile(biome=biome, resources=self._spawn_resources(biome)))
            tiles.append(row)
        return World(width=width, height=height, tiles=tiles)

    def _choose_biome(self, x: int, y: int) -> Biome:
        # Lightweight pseudo-noise blend from coordinates + seeded randomness.
        v = (x * 73856093 ^ y * 19349663) % 100
        n = (v + self._rng.randint(0, 99)) / 2
        if n < 15:
            return Biome.WATER
        if n < 35:
            return Biome.DESERT
        if n < 60:
            return Biome.PLAINS
        if n < 82:
            return Biome.FOREST
        return Biome.HILLS

    def _spawn_resources(self, biome: Biome) -> dict[str, int]:
        if biome == Biome.WATER:
            return {"food": self._rng.randint(1, 5), "wood": 0, "stone": 0}
        if biome == Biome.DESERT:
            return {"food": self._rng.randint(0, 2), "wood": 0, "stone": self._rng.randint(1, 4)}
        if biome == Biome.PLAINS:
            return {
                "food": self._rng.randint(4, 10),
                "wood": self._rng.randint(1, 4),
                "stone": self._rng.randint(1, 3),
            }
        if biome == Biome.FOREST:
            return {
                "food": self._rng.randint(2, 7),
                "wood": self._rng.randint(5, 12),
                "stone": self._rng.randint(0, 2),
            }
        # hills
        return {
            "food": self._rng.randint(1, 4),
            "wood": self._rng.randint(1, 3),
            "stone": self._rng.randint(4, 10),
        }
