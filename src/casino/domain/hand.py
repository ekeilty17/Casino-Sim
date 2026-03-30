from dataclasses import dataclass
from typing import List

from casino.domain.card import Card

@dataclass
class Hand:
    cards: List[Card]