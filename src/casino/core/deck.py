import random
from typing import List, Optional, Iterator, Iterable

from core.card import Pip, Suit, Card


class DeckExhaustedError(Exception):
    """Raised when attempting to deal more cards than remain."""


class Deck:
    """
    Represents one or more standard 52-card decks.

    The deck is internally modeled as a contiguous list with a moving index:

        [ dealt cards | remaining cards ]
                       ^ index

    - Dealing advances the index
    - Shuffling resets the index
    - No cards are physically removed during dealing
    """

    def __init__(self, number_of_decks: int = 1, seed: Optional[int] = None) -> None:
        if number_of_decks <= 0:
            raise ValueError("number_of_decks must be positive")

        self._number_of_decks = number_of_decks
        self._rng = random.Random(seed)

        self._cards: List[Card] = []
        self._index: int = 0

        self.reset()

    # -------------------
    # Representation
    # -------------------

    def __repr__(self) -> str:
        return f"Deck(decks={self._number_of_decks}, remaining={self.num_cards_remaining()})"

    def __str__(self) -> str:
        return " ".join(str(card) for card in self._cards[self._index:])

    def __iter__(self) -> Iterator[Card]:
        return iter(self._cards[self._index:])

    # -------------------
    # State
    # -------------------

    def size(self) -> int:
        return len(self._cards)

    def num_cards_remaining(self) -> int:
        return self.size() - self._index

    def num_cards_dealt(self) -> int:
        return self._index

    def get_cards(self) -> List[Card]:
        return list(self._cards)

    def get_dealt_cards(self) -> List[Card]:
        return self._cards[:self._index]

    def get_remaining_cards(self) -> List[Card]:
        return self._cards[self._index:]

    # -------------------
    # Core actions
    # -------------------

    def deal(self, num_cards: int = 1) -> List[Card]:
        """
        Deal cards from the top of the remaining portion of the deck.
        """
        if num_cards <= 0:
            raise ValueError("num_cards must be positive")

        if self._index + num_cards > len(self._cards):
            raise DeckExhaustedError("Not enough cards remaining")

        start = self._index
        end = self._index + num_cards
        self._index = end

        return self._cards[start:end]

    def burn(self, num_cards: int = 1) -> None:
        """
        Discard cards without returning them to the deck.
        """
        self.deal(num_cards)

    def shuffle(self) -> None:
        """
        Shuffle the entire deck and reset dealing position.
        """
        self._rng.shuffle(self._cards)
        self._index = 0

    def reset(self) -> None:
        """
        Reset deck to a fresh ordered state.
        """
        self._cards = [
            card
            for _ in range(self._number_of_decks)
            for card in self._new_deck_order()
        ]
        self._index = 0

    def stack(self, cards: Iterable[Card]) -> None:
        """
        Replace the deck with a specific ordered set of cards.
        """
        cards = list(cards)
        self._assert_valid_deck(cards)

        self._cards = cards
        self._index = 0

    def cut(self, num_cards: Optional[int] = None) -> None:
        """
        Cut the deck within the remaining portion.

        Moves a portion of the top of the remaining cards to the bottom
        of the remaining section.
        """
        remaining = self.num_cards_remaining()

        if remaining <= 1:
            return

        if num_cards is None:
            num_cards = self._rng.randint(1, remaining - 1)

        if not (0 <= num_cards < remaining):
            raise ValueError("num_cards out of range")

        if num_cards == 0:
            return

        start = self._index
        cut_point = start + num_cards

        self._cards[start:] = (
            self._cards[cut_point:] +
            self._cards[start:cut_point]
        )

    # -------------------
    # Internal helpers
    # -------------------

    def _new_deck_order(self) -> List[Card]:
        """
        Return a single standard deck in canonical order.
        """
        cards: List[Card] = []

        for suit in Suit:
            pips = reversed(Pip) if suit in {Suit.DIAMOND, Suit.SPADE} else Pip
            for pip in pips:
                cards.append(Card(pip, suit))

        return cards

    def _assert_valid_deck(self, cards: Iterable[Card]) -> None:
        """
        Validate that the provided cards match the expected composition
        of the configured number of decks.
        """
        expected = [
            card
            for _ in range(self._number_of_decks)
            for card in self._new_deck_order()
        ]

        actual = list(cards)

        if len(expected) != len(actual):
            raise ValueError(
                f"Unexpected number of cards: got {len(actual)}, expected {len(expected)}"
            )

        if set(expected) != set(actual):
            raise ValueError("Deck is missing cards or contains duplicates.")