from __future__ import annotations
from dataclasses import dataclass

from casino.core.suit import Suit
from casino.core.rank import Rank


@dataclass(frozen=True, slots=True)
class Card:
    """
    Immutable representation of a playing card.

    Attributes:
        rank: Rank of the card
        suit: Suit of the card
    """

    rank: Rank
    suit: Suit

    def __post_init__(self) -> None:
        if not isinstance(self.rank, Rank):
            raise TypeError("pip must be a Pip enum")
        if not isinstance(self.suit, Suit):
            raise TypeError("suit must be a Suit enum")

    def __str__(self) -> str:
        """
        Short human-readable representation, e.g. 'A♠', '10♦'
        """
        return f"{self.rank.symbol}{self.suit.symbol}"

    def __repr__(self) -> str:
        return f"Card(pip={self.rank.name}, suit={self.suit.name})"

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit