from dataclasses import dataclass

from core.player import Player

@dataclass
class BlackjackSpot:
    player: Player
    bet: int