from enum import Enum
from functools import total_ordering

@total_ordering
class Rank(Enum):
    """
    Represents the rank of a playing card.

    Value structure:
        (name, display_symbol)
    """

    ACE = ("A", 1)
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 11)
    QUEEN = ("Q", 12)
    KING = ("K", 13)

    def __init__(self, symbol: str, order: int) -> None:
        self._symbol = symbol
        self._order = order

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def order(self) -> int:
        return self._order

    def __str__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return f"Pip.{self.name}"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        return self._order < other._order