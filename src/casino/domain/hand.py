from dataclasses import dataclass, field
from typing import List

from casino.domain.card import Card

@dataclass
class Hand:
    bet: int
    cards: List[Card] = field(default_factory=list)