from dataclasses import dataclass

from ..decision import DecisionStrategy
from ..betting import BettingStrategy
from .action import Action

@dataclass
class Player:
    player_id: int
    name: str
    bankroll: int
    decision_strategy: DecisionStrategy
    betting_strategy: BettingStrategy

    # TODO: Need to pass in some type of context
    def place_bet(self, context) -> int:
        """Determine bet using the betting strategy and update bankroll."""
        amount = self.betting_strategy.bet(context)
        if amount > self.bankroll:
            raise ValueError(f"Player {self.name} cannot bet more than bankroll")
        self.bankroll -= amount
        return amount

    def receive_payout(self, amount: int):
        """Add winnings back to bankroll."""
        self.bankroll += amount

    # TODO: Need to pass in some type of context
    def make_decision(self, context) -> Action:
        """Ask the strategy for next move."""
        return self.decision_strategy.decide(context)