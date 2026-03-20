import random 
from typing import List
from casino.roulette.core.number import RouletteNumber

class RouletteWheel:

    def __init__(self):
        self._wheel: List[RouletteNumber] = [number for number in RouletteNumber]

    def spin(self) -> RouletteNumber:
        return random.choice(self._wheel)