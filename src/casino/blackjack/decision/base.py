from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Union, Set

from casino.domain import Card
from casino.blackjack.domain import Action, PlayerHand, DealerHand

@dataclass(frozen=True)
class DecisionContext:
    dealer_upcard: Card
    hand: Union[PlayerHand, DealerHand]
    actions: Set[Action]
    num_decks: int
    dealer_hits_soft_17: bool
    dealer_peak: bool
    double_after_split: bool

class DecisionStrategy(ABC):

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def decide(self, context: DecisionContext) -> Action:
        """
        Given the current blackjack state, return the next action.
        """
        pass