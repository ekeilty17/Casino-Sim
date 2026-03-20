import pytest
from casino.core.deck import Deck, DeckExhaustedError
from casino.core.card import Card, Pip, Suit


# -------------------
# Helpers
# -------------------

def assert_valid_deck_state(deck: Deck) -> None:
    """Common invariant checks."""
    assert deck.num_cards_dealt() + deck.num_cards_remaining() == len(deck)
    assert deck.num_cards_dealt() >= 0
    assert deck.num_cards_remaining() >= 0
    assert len(deck.get_cards()) == len(deck)


# -------------------
# Initialization
# -------------------

def test_deck_initialization_single_deck():
    deck = Deck(number_of_decks=1)

    assert len(deck) == 52
    assert deck.num_cards_remaining() == 52
    assert deck.num_cards_dealt() == 0
    assert_valid_deck_state(deck)


def test_deck_initialization_multiple_decks():
    deck = Deck(number_of_decks=2)

    assert len(deck) == 2*52
    assert deck.num_cards_remaining() == 2*52
    assert deck.num_cards_dealt() == 0
    assert_valid_deck_state(deck)


def test_invalid_number_of_decks():
    with pytest.raises(ValueError):
        Deck(number_of_decks=0)


# -------------------
# Dealing
# -------------------

def test_deal_cards():
    deck = Deck(number_of_decks=1, seed=42)
    deck.shuffle()

    cards = deck.deal(5)

    assert len(cards) == 5
    assert deck.num_cards_dealt() == 5
    assert deck.num_cards_remaining() == 52 - 5
    assert_valid_deck_state(deck)


def test_deal_single_card():
    deck = Deck(number_of_decks=1)
    card = deck.deal(1)

    assert len(card) == 1
    assert deck.num_cards_dealt() == 1
    assert deck.num_cards_remaining() == 52 - 1


def test_deal_exhaustion():
    deck = Deck(number_of_decks=1)

    with pytest.raises(DeckExhaustedError):
        deck.deal(53)


def test_burn_cards():
    deck = Deck(number_of_decks=1)

    deck.burn(10)

    assert deck.num_cards_dealt() == 10
    assert deck.num_cards_remaining() == 52 - 10
    assert_valid_deck_state(deck)


def test_burn_exhaustion():
    deck = Deck(number_of_decks=1)

    with pytest.raises(DeckExhaustedError):
        deck.burn(53)


# -------------------
# Shuffle
# -------------------

def test_shuffle_resets_index():
    deck = Deck(number_of_decks=1, seed=1)

    deck.deal(10)
    assert deck.num_cards_dealt() == 10

    deck.shuffle()

    assert deck.num_cards_dealt() == 0
    assert deck.num_cards_remaining() == 52
    assert_valid_deck_state(deck)


def test_deterministic_shuffle():
    d1 = Deck(number_of_decks=1, seed=123)
    d2 = Deck(number_of_decks=1, seed=123)

    d1.shuffle()
    d2.shuffle()

    assert d1.get_cards() == d2.get_cards()


# -------------------
# Reset
# -------------------

def test_reset():
    deck = Deck(number_of_decks=1)

    deck.deal(20)
    deck.reset()

    assert deck.num_cards_dealt() == 0
    assert deck.num_cards_remaining() == 52
    assert_valid_deck_state(deck)


# -------------------
# Iteration
# -------------------

def test_iteration_returns_remaining_cards():
    deck = Deck(number_of_decks=1)

    deck.deal(10)

    remaining = list(deck)

    assert len(remaining) == 52 - 10
    assert_valid_deck_state(deck)


# -------------------
# Cut
# -------------------

def test_cut_preserves_cards():
    deck = Deck(number_of_decks=1, seed=1)
    deck.shuffle()

    original_cards = set(deck.get_cards())

    deck.cut(10)

    assert set(deck.get_cards()) == original_cards
    assert len(deck) == 52
    assert_valid_deck_state(deck)


def test_cut_random():
    deck = Deck(number_of_decks=1, seed=1)
    deck.shuffle()

    original_order = deck.get_cards()

    deck.cut()

    # Should still contain same cards, but order likely changed
    assert set(deck.get_cards()) == set(original_order)
    assert_valid_deck_state(deck)


# -------------------
# Stack
# -------------------

def test_stack():
    deck = Deck(number_of_decks=1)

    cards = deck.get_cards()
    deck.stack(cards)

    assert deck.get_cards() == cards
    assert deck.num_cards_dealt() == 0
    assert_valid_deck_state(deck)


# -------------------
# Representation
# -------------------

def test_repr_and_str():
    deck = Deck(number_of_decks=1)

    r = repr(deck)
    s = str(deck)

    assert "Deck" in r
    assert isinstance(s, str)


# -------------------
# Invariants under operations
# -------------------

def test_invariants_after_operations():
    deck = Deck(number_of_decks=1, seed=42)
    deck.shuffle()

    for _ in range(len(deck)):
        deck.deal(1)
        assert_valid_deck_state(deck)

    with pytest.raises(DeckExhaustedError):
        deck.burn(1)