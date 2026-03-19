from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering


@total_ordering
class Pip(Enum):
    """
    Represents the rank of a playing card.
    """

    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

    @property
    def order(self) -> int:
        order_map = {
            Pip.ACE: 1,
            Pip.TWO: 2,
            Pip.THREE: 3,
            Pip.FOUR: 4,
            Pip.FIVE: 5,
            Pip.SIX: 6,
            Pip.SEVEN: 7,
            Pip.EIGHT: 8,
            Pip.NINE: 9,
            Pip.TEN: 10,
            Pip.JACK: 11,
            Pip.QUEEN: 12,
            Pip.KING: 13,
        }
        return order_map[self]

    def __lt__(self, other: "Pip") -> bool:
        if not isinstance(other, Pip):
            return NotImplemented
        return self.order < other.order

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pip):
            return NotImplemented
        return self._order == other._order

    def __lt__(self, other: Pip) -> bool:
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
        return {
            Suit.HEART: "♥",
            Suit.CLUB: "♣",
            Suit.DIAMOND: "♦",
            Suit.SPADE: "♠",
        }[self]

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