from dataclasses import dataclass

@dataclass(frozen=True)
class BlackjackTable:
    num_decks: int
    deck_penetration: float
    num_spots: int
    min_bet: int
    max_bet: int

    # TODO: I could add side-bets eventually here