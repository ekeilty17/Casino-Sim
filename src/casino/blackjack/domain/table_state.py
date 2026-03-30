from dataclasses import dataclass, field
from typing import List, Any, Optional

from .hand import DealerHand
from .spot import Spot

@dataclass
class TableState:
    dealer_hand: DealerHand
    spots: List[Spot] = field(default_factory=list)