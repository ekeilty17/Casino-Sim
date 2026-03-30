import random
from typing import Optional

from casino.blackjack.domain import Action

from .base import DecisionStrategy, DecisionContext

class RandomDecisionStrategy(DecisionStrategy):

    def __init__(self, seed: Optional[int]=None):
        self._seed = seed
        self._rng = random.Random(self._seed)

    def decide(self, context: DecisionContext) -> Action:
        return self._rng.choice(context.actions)