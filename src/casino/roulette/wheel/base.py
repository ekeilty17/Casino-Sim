import random
from typing import List
from abc import ABC, abstractmethod

from ..domain import RouletteNumber

class RouletteWheel(ABC):
    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._wheel: List[RouletteNumber] = self.construct_wheel()

    @abstractmethod
    def construct_wheel(self) -> List[RouletteNumber]:
        """
        Abstract method that must be implemented in a subclass to
        define how the roulette wheel is constructed.
        """
        pass

    def spin(self) -> RouletteNumber:
        """
        Simulate a spin of the roulette wheel by choosing a random number
        from the wheel.
        """
        return self._rng.choice(self._wheel)