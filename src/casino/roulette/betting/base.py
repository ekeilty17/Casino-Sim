from dataclasses import dataclass
from abc import ABC, abstractmethod

from ..domain import BetCatalog

@dataclass(frozen=True)
class BettingContext:
    catalog: BetCatalog
    bankroll: int
    table_max: int = 0
    table_min: int | None = None

class BettingStrategy(ABC):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def bet(self, context: BettingContext) -> int:
        """
        Determine the wager amount for the next round.
        Must respect table limits and bankroll constraints.
        """
        pass