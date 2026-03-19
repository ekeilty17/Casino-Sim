from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering


from enum import Enum
from functools import total_ordering

@total_ordering
class Pip(Enum):
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
        if not isinstance(other, Pip):
            return NotImplemented
        return self._order < other._order

class Suit(Enum):
    """
    Represents the suit of a playing card.

    Value structure:
        (name, display_symbol)
    """

    HEART = "heart"
    CLUB = "club"
    DIAMOND = "diamond"
    SPADE = "spade"

    @property
    def symbol(self) -> str:
        """Return a terminal-friendly display symbol for the suit."""
        SUIT_SYMBOLS = {
            "heart": "♥",
            "club": "♣",
            "diamond": "♦",
            "spade": "♠",
        }
        return SUIT_SYMBOLS[self.value]

    def __str__(self) -> str:
        return self.symbol


@dataclass(frozen=True, slots=True)
class Card:
    """
    Immutable representation of a playing card.

    Attributes:
        pip: Rank of the card
        suit: Suit of the card
    """

    pip: Pip
    suit: Suit

    def __post_init__(self) -> None:
        if not isinstance(self.pip, Pip):
            raise TypeError("pip must be a Pip enum")
        if not isinstance(self.suit, Suit):
            raise TypeError("suit must be a Suit enum")

    def __str__(self) -> str:
        """
        Short human-readable representation, e.g. 'A♠', '10♦'
        """
        return f"{self.pip.symbol}{self.suit.symbol}"

    def __repr__(self) -> str:
        return f"Card(pip={self.pip.name}, suit={self.suit.name})"

    def __hash__(self) -> int:
        return hash((self.pip, self.suit))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.pip == other.pip and self.suit == other.suit