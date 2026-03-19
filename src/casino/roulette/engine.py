import random
from typing import List

from roulette.core.number import RoutelletNumber
from core.player import Player

class RouletteEngine:

    def __init__(
        self, 
        players: List[Player]
    ):  
        self.players = players
        self._wheel: List[RoutelletNumber] = [number for number in RoutelletNumber]

    def run(self):
        pass

    def spin(self) -> RoutelletNumber:
        return random.choice(self._wheel)