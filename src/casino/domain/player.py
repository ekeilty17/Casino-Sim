from dataclasses import dataclass

@dataclass
class Player:
    player_id: int
    name: str
    bankroll: int