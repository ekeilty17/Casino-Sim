from enum import Enum

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
