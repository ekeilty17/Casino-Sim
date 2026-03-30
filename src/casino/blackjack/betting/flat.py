from .base import BettingStrategy, BettingContext

class FlatBettingStrategy(BettingStrategy):

    def __init__(self, amount: int=10):
        self.amount = amount

    def __repr__(self) -> str:
        return f"FlatBettingStrategy(amount={self.amount})"

    def __str__(self) -> str:
        return f"FlatBettingStrategy(amount={self.amount})"

    def bet(self, context: BettingContext) -> int:
        return min(
            max(self.amount, context.min_bet),
            context.max_bet,
            context.bankroll
        )