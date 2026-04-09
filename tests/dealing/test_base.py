import pytest
from casino.domain import Deck, Card, Rank, Suit
from casino.dealing import DealingDevice
from casino.domain.deck import DeckExhaustedError

from .conftest import assert_valid_dealing_device_state


# -------------------
# Concrete implementation for testing
# -------------------

class SimpleDealingDevice(DealingDevice):
    """Minimal concrete implementation for testing the base class."""
    
    def __init__(self, deck: Deck):
        super().__init__(deck)
        self._discarded_cards = []
    
    def discard(self, *cards: Card) -> None:
        self._discarded_cards.extend(cards)
    
    def shuffle(self) -> None:
        self.fair_shuffle()
        self._discarded_cards.clear()
    
    def get_discarded(self):
        return list(self._discarded_cards)


# -------------------
# Initialization
# -------------------

def test_dealing_device_initialization():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    assert len(device) == 52
    assert device.num_cards_remaining() == 52
    assert device.num_cards_dealt() == 0
    assert_valid_dealing_device_state(device)


def test_dealing_device_requires_deck():
    with pytest.raises(ValueError, match="deck cannot be None"):
        SimpleDealingDevice(None)


def test_dealing_device_with_multiple_decks():
    deck = Deck(number_of_decks=6, seed=42)
    device = SimpleDealingDevice(deck)
    
    assert len(device) == 6 * 52
    assert device.num_cards_remaining() == 6 * 52
    assert device.num_cards_dealt() == 0
    assert_valid_dealing_device_state(device)


# -------------------
# Representation
# -------------------

def test_dealing_device_str():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    s = str(device)
    assert "SimpleDealingDevice" in s
    assert "Deck" in s


def test_dealing_device_repr():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    r = repr(device)
    assert "SimpleDealingDevice" in r
    assert "deck=" in r


# -------------------
# Dealing cards
# -------------------

def test_deal_single_card():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    cards = device.deal(1)
    
    assert len(cards) == 1
    assert isinstance(cards[0], Card)
    assert device.num_cards_dealt() == 1
    assert device.num_cards_remaining() == 51
    assert_valid_dealing_device_state(device)


def test_deal_multiple_cards():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    cards = device.deal(5)
    
    assert len(cards) == 5
    assert all(isinstance(card, Card) for card in cards)
    assert device.num_cards_dealt() == 5
    assert device.num_cards_remaining() == 47
    assert_valid_dealing_device_state(device)


def test_deal_invalid_num_cards():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    with pytest.raises(ValueError, match="num_cards must be positive"):
        device.deal(0)
    
    with pytest.raises(ValueError, match="num_cards must be positive"):
        device.deal(-1)


def test_deal_exhaustion():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    device.deal(52)
    
    with pytest.raises(DeckExhaustedError):
        device.deal(1)


def test_next_card():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    card = device.next_card()
    
    assert isinstance(card, Card)
    assert device.num_cards_dealt() == 1
    assert device.num_cards_remaining() == 51
    assert_valid_dealing_device_state(device)


def test_next_card_returns_same_as_deal_one():
    deck1 = Deck(number_of_decks=1, seed=42)
    deck2 = Deck(number_of_decks=1, seed=42)
    device1 = SimpleDealingDevice(deck1)
    device2 = SimpleDealingDevice(deck2)
    
    card1 = device1.next_card()
    card2 = device2.deal(1)[0]
    
    assert card1 == card2


# -------------------
# Burning cards
# -------------------

def test_burn_single_card():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    device.burn(1)
    
    assert device.num_cards_dealt() == 1
    assert device.num_cards_remaining() == 51
    assert_valid_dealing_device_state(device)


def test_burn_multiple_cards():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    device.burn(10)
    
    assert device.num_cards_dealt() == 10
    assert device.num_cards_remaining() == 42
    assert_valid_dealing_device_state(device)


def test_burn_invalid_num_cards():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    with pytest.raises(ValueError, match="num_cards must be positive"):
        device.burn(0)
    
    with pytest.raises(ValueError, match="num_cards must be positive"):
        device.burn(-1)


def test_burn_exhaustion():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    device.burn(52)
    
    with pytest.raises(DeckExhaustedError):
        device.burn(1)


# -------------------
# Discarding
# -------------------

def test_discard_single_card():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    card = device.next_card()
    device.discard(card)
    
    discarded = device.get_discarded()
    assert len(discarded) == 1
    assert discarded[0] == card


def test_discard_multiple_cards():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    cards = device.deal(5)
    device.discard(*cards)
    
    discarded = device.get_discarded()
    assert len(discarded) == 5
    assert discarded == cards


# -------------------
# Shuffling
# -------------------

def test_fair_shuffle_resets_deck():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    device.deal(20)
    assert device.num_cards_dealt() == 20
    
    device.fair_shuffle()
    
    assert device.num_cards_dealt() == 0
    assert device.num_cards_remaining() == 52
    assert_valid_dealing_device_state(device)


def test_shuffle_clears_discards():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    cards = device.deal(5)
    device.discard(*cards)
    assert len(device.get_discarded()) == 5
    
    device.shuffle()
    
    assert len(device.get_discarded()) == 0
    assert device.num_cards_dealt() == 0
    assert device.num_cards_remaining() == 52


def test_fair_shuffle_is_deterministic_with_seed():
    deck1 = Deck(number_of_decks=1, seed=123)
    deck2 = Deck(number_of_decks=1, seed=123)
    device1 = SimpleDealingDevice(deck1)
    device2 = SimpleDealingDevice(deck2)
    
    device1.fair_shuffle()
    device2.fair_shuffle()
    
    cards1 = device1.deal(10)
    cards2 = device2.deal(10)
    
    assert cards1 == cards2


# -------------------
# State tracking
# -------------------

def test_num_cards_dealt():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    assert device.num_cards_dealt() == 0
    
    device.deal(10)
    assert device.num_cards_dealt() == 10
    
    device.deal(5)
    assert device.num_cards_dealt() == 15


def test_num_cards_remaining():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    assert device.num_cards_remaining() == 52
    
    device.deal(10)
    assert device.num_cards_remaining() == 42
    
    device.deal(5)
    assert device.num_cards_remaining() == 37


def test_len_returns_total_cards():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    assert len(device) == 52
    
    device.deal(20)
    assert len(device) == 52  # Total doesn't change


# -------------------
# needs_shuffle
# -------------------

def test_needs_shuffle_default_false():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    assert device.needs_shuffle() is False
    
    device.deal(40)
    assert device.needs_shuffle() is False


# -------------------
# Invariants
# -------------------

def test_invariants_maintained_throughout_dealing():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    for i in range(52):
        assert_valid_dealing_device_state(device)
        device.deal(1)
    
    assert_valid_dealing_device_state(device)


def test_invariants_after_shuffle():
    deck = Deck(number_of_decks=1, seed=42)
    device = SimpleDealingDevice(deck)
    
    device.deal(30)
    device.shuffle()
    
    assert_valid_dealing_device_state(device)
    assert device.num_cards_dealt() == 0
    assert device.num_cards_remaining() == 52