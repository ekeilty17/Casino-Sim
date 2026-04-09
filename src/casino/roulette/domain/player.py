from dataclasses import dataclass

@dataclass
class Player:
    player_id: int
    name: str
    bankroll: int
    # betting_strategy: BettingStrategy

    # TODO: Need to pass in some type of context
    def place_bets(self, context) -> int:
        """Determine bet using the betting strategy and update bankroll."""
        # amount = self.betting_strategy.bet(context)
        # if amount > self.bankroll:
        #     raise ValueError(f"Player {self.name} cannot bet more than bankroll")
        # self.bankroll -= amount
        # return amount
        return 10