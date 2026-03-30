import random
from typing import Optional

from .base import BettingStrategy, BettingContext

class RandomBettingStrategy(BettingStrategy):

    def __init__(self, seed: Optional[int]=None):
        self._seed = seed
        self._rng = random.Random(self._seed)

    def bet(self, context: BettingContext) -> int:
        lower = context.min_bet
        upper = min(context.bankroll, context.max_bet) if context.max_bet else context.bankroll
        return self._rng.randint(lower, upper)