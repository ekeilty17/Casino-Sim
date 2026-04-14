import random
from typing import List, Set

from ..domain import RouletteNumber

class RouletteWheel:
    def __init__(self, num_zeros: int, num_balls: int, seed: int | None = None) -> None:
        self.num_zeros = num_zeros
        self.num_balls = num_balls
        self._rng = random.Random(seed)
        self._wheel: List[RouletteNumber] = self._construct_wheel()

    def _construct_wheel(self) -> List[RouletteNumber]:
        wheel = [number for number in RouletteNumber if not number.is_zero_value()]
        if self.num_zeros >= 1:
            wheel.append(RouletteNumber.ZERO)
        if self.num_zeros >= 2:
            wheel.append(RouletteNumber.DOUBLE_ZERO)
        if self.num_zeros >= 3:
            wheel.append(RouletteNumber.TRIPLE_ZERO)
        return wheel

    def spin(self) -> Set[RouletteNumber]:
        """
        Simulate a spin of the roulette wheel by choosing a random number
        from the wheel.
        """
        winning_numbers = self._rng.sample(self._wheel, k=self.num_balls)
        return set(winning_numbers)