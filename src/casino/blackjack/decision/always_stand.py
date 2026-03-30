from casino.blackjack.domain import Action

from .base import DecisionStrategy, DecisionContext

class AlwaysStandDecisionStrategy(DecisionStrategy):

    def decide(self, context: DecisionContext) -> Action:
        return Action.STAND