from abc import ABC, abstractmethod
from typing import List

from core.deck import Deck
from core.card import Card


class CardDealingDevice(ABC):
    """
    Abstract base class for all card dealing devices (e.g., Shoe, CSM).

    This class is intentionally minimal and delegates game-specific behavior
    (like discarding and shuffling policies) to subclasses. 
    
    The application is responsible for deciding when a round ends and when to call `shuffle()`.
    This class includes `needs_shuffle()` which gives a signal to the application that `shuffle()` 
    should be called at the end of the round
    """

    def __init__(self, deck: Deck):
        if deck is None:
            raise ValueError("deck cannot be None")

        self._deck = deck

    # -------------------
    # Representation
    # -------------------

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._deck})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(deck={repr(self._deck)})"

    # -------------------
    # Deck state
    # -------------------

    def size(self) -> int:
        return self._deck.size()

    def num_cards_dealt(self) -> int:
        dealt = self._deck.num_cards_dealt()

        if dealt < 0 or dealt > self.size():
            raise RuntimeError("Invalid deck state: num_cards_dealt out of bounds")

        return dealt

    def num_cards_remaining(self) -> int:
        remaining = self._deck.num_cards_remaining()

        if remaining < 0 or remaining > self.size():
            raise RuntimeError("Invalid deck state: num_cards_remaining out of bounds")

        return remaining

    # -------------------
    # Core actions
    # -------------------

    def deal(self, num_cards: int = 1) -> List[Card]:
        """
        Deal cards from the device.

        Subclasses may override to enforce additional rules
        (e.g., cut card behavior in a Shoe).
        """
        if num_cards <= 0:
            raise ValueError("num_cards must be positive")

        return self._deck.deal(num_cards)

    def burn(self, num_cards: int = 1) -> None:
        """
        Burn cards from the device.

        Subclasses may override if burn behavior differs
        (e.g., tracking burn cards explicitly).
        """
        if num_cards <= 0:
            raise ValueError("num_cards must be positive")

        self._deck.burn(num_cards)

    # -------------------
    # Abstract behavior
    # -------------------

    @abstractmethod
    def discard(self, *cards: Card) -> None:
        """
        Handle discarded cards.

        This is intentionally abstract because different dealing devices
        handle discards differently:

        - Shoe: accumulate in discard tray
        - Continuous shuffler: reinsert into deck
        - Simple deck: ignore or track externally
        """
        raise NotImplementedError

    @abstractmethod
    def shuffle(self) -> None:
        """
        Shuffle or reset the dealing device.

        Implementations define what 'shuffle' means:
        - Shoe: reset deck + reshuffle + reset cut card
        - CSM: may be a no-op or continuous process
        """
        raise NotImplementedError

    # -------------------
    # Optional extension points
    # -------------------

    def needs_shuffle(self) -> bool:
        """
        Indicates whether the device recommends a shuffle.

        Default: never required.
        Subclasses (e.g., Shoe) should override.
        """
        return False