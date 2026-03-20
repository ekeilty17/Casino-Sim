import math
import random
from typing import List, Optional

from casino.core.deck import Deck
from casino.core.card import Card
from casino.card_dealing_devices.card_dealing_device import CardDealingDevice


class Shoe(CardDealingDevice):
    """
    Models a casino-style shoe with a cut card and discard tray.

    Key behaviors:
    - Cards are dealt sequentially from the deck
    - Discards are accumulated in a discard tray
    - A cut card determines when a shuffle is required
    - Shuffle resets deck and discard tray

    This implementation SIGNALS when a shuffle is needed via `needs_shuffle()`,
    but does NOT enforce it (caller decides policy).
    """

    _EPSILON = 1e-6

    def __init__(
        self,
        deck: Deck,
        penetration: float,
        penetration_variance: float = 0.0,
        seed: Optional[int] = None,
    ):
        super().__init__(deck)

        if not (0.0 < penetration < 1.0):
            raise ValueError("penetration must be between 0 and 1 (exclusive)")

        if penetration_variance < 0:
            raise ValueError("penetration_variance must be non-negative")

        self._penetration = penetration
        self._penetration_variance = penetration_variance
        self._rng = random.Random(seed)

        self._discard_tray: List[Card] = []
        self._cut_card_index: int = 0

        self._update_cut_card()

    # -------------------
    # Representation
    # -------------------

    def __str__(self) -> str:
        return (
            f"Shoe("
            f"remaining={self.num_cards_remaining()}, "
            f"dealt={self.num_cards_dealt()}, "
            f"cut_card={self.cut_card_index()}, "
            f"needs_shuffle={self.needs_shuffle()}"
            f")"
        )

    def __repr__(self) -> str:
        return (
            f"Shoe("
            f"cards_remaining={self.num_cards_remaining()}, "
            f"cards_dealt={self.num_cards_dealt()}, "
            f"cut_card_index={self.cut_card_index()}, "
            f"penetration={self._penetration:.4f}, "
            f"variance={self._penetration_variance:.4f}"
            f")"
        )

    # -------------------
    # Getters
    # -------------------

    def discard_tray(self) -> List[Card]:
        """
        Returns a copy of the discard tray.
        """
        return list(self._discard_tray)

    def cut_card_index(self) -> int:
        """
        Exposes cut card position for testing and observability.
        """
        return self._cut_card_index

    # -------------------
    # Core actions
    # -------------------

    def burn(self, num_cards: int = 1) -> None:
        """
        Burn cards and place them into the discard tray.
        """
        if num_cards <= 0:
            raise ValueError("num_cards must be positive")

        burned_cards = self._deck.deal(num_cards)
        self._discard_tray.extend(burned_cards)

    def discard(self, *cards: Card) -> None:
        """
        Add cards to the discard tray.
        """
        for card in cards:
            if card is None:
                raise ValueError("Cannot discard None")

            self._discard_tray.append(card)

    def shuffle(self) -> None:
        """
        Reset and shuffle the shoe.
        """
        self.fair_shuffle()

        self._discard_tray.clear()
        self._update_cut_card()
    
    def needs_shuffle(self) -> bool:
        """
        Returns True if the cut card has been reached.
        """
        return self.num_cards_dealt() >= self._cut_card_index

    # -------------------
    # Internal helpers
    # -------------------

    def _update_cut_card(self) -> None:
        """
        Computes the cut card index based on penetration and variance.
        """
        perturbation = 0.0

        if self._penetration_variance > 0.0:
            std_dev = math.sqrt(self._penetration_variance)
            perturbation = self._rng.gauss(0.0, std_dev)

        penetration = self._penetration + perturbation

        # Clamp to safe operational bounds (avoid 0 and 1 exactly)
        penetration = max(self._EPSILON, min(1.0 - self._EPSILON, penetration))

        self._cut_card_index = int(len(self._deck) * penetration)

        # Defensive invariant
        if not (0 <= self._cut_card_index <= len(self._deck)):
            raise RuntimeError("Invalid cut card index computed")