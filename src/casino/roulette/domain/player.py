from dataclasses import dataclass
from typing import List

from casino.roulette.domain.limits import Limits

from . import Bet, BetDefinition, BetKind, BetCatalog, RouletteNumber

@dataclass
class Player:
    player_id: int
    name: str
    bankroll: int
    # betting_strategy: BettingStrategy

    def __hash__(self) -> int:
        return self.player_id

    # TODO: Need to pass in some type of context
    def place_bets(
        self, 
        catalog: BetCatalog,
        table_limits: Limits
    ) -> List[Bet]:
        """Determine bet using the betting strategy and update bankroll."""
        stake = 10
        if stake > self.bankroll:
            raise ValueError(f"Player {self.name} cannot bet more than bankroll")
        self.bankroll -= stake
        
        return [Bet(
            definition=BetDefinition(
                name="straight",
                bet_type=BetKind.STRAIGHT,
                payout=35
            ),
            wagered_numbers=(RouletteNumber.EIGHT, ),
            stake=10
        )]

    def receive_payout(self, amount: int):
        """Add winnings back to bankroll."""
        self.bankroll += amount