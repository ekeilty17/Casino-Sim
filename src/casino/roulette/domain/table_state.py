from dataclasses import dataclass, field
from typing import Set, List, Dict

from . import Player, RouletteNumber, Bet

@dataclass
class TableState:
    bets_open: bool = True
    bets: Dict[Player, List[Bet]] = field(default_factory=dict)
    winning_numbers: Set[RouletteNumber] = field(default_factory=set)