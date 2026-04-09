from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class BettingContext:
    bankroll: int
    min_bet: int = 0
    max_bet: int | None = None

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