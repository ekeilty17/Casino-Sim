from casino.blackjack.domain import Action

from .base import DecisionStrategy, DecisionContext

class DealerDecisionStrategy(DecisionStrategy):

    def decide(self, context: DecisionContext) -> Action:
        if context.hand.get_total() < 17:
            return Action.HIT
        if context.hand.get_total() == 17 and context.hand.is_soft():
            return Action.HIT if context.dealer_hits_soft_17 else Action.STAND
        return Action.STAND