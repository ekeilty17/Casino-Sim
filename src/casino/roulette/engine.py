import random
from typing import List

from .domain import RouletteNumber, RoulettePlayer
from .wheel import RouletteWheel

class RouletteEngine:

    def __init__(
        self, 
        players: List[RoulettePlayer],
        wheel: RouletteWheel
    ):  
        self.players = players
        self.wheel = wheel

    def run(self):
        pass