import pytest
from casino.domain import Deck, Card, Rank, Suit
from casino.dealing import Shoe
from casino.domain.deck import DeckExhaustedError

from .conftest import assert_valid_dealing_device_state


# -------------------
# Initialization
# -------------------

def test_shoe_initialization():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    assert len(shoe) == 6 * 52
    assert shoe.num_cards_remaining() == 6 * 52
    assert shoe.num_cards_dealt() == 0
    assert len(shoe.discard_tray()) == 0
    assert_valid_dealing_device_state(shoe)


def test_shoe_initialization_with_variance():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.05, seed=123)
    
    assert len(shoe) == 6 * 52
    assert shoe.num_cards_remaining() == 6 * 52
    assert shoe.num_cards_dealt() == 0
    assert_valid_dealing_device_state(shoe)


def test_shoe_invalid_penetration_zero():
    deck = Deck(number_of_decks=6, seed=42)
    
    with pytest.raises(ValueError, match="penetration must be between 0 and 1"):
        Shoe(deck, penetration=0.0)


def test_shoe_invalid_penetration_one():
    deck = Deck(number_of_decks=6, seed=42)
    
    with pytest.raises(ValueError, match="penetration must be between 0 and 1"):
        Shoe(deck, penetration=1.0)


def test_shoe_invalid_penetration_negative():
    deck = Deck(number_of_decks=6, seed=42)
    
    with pytest.raises(ValueError, match="penetration must be between 0 and 1"):
        Shoe(deck, penetration=-0.5)


def test_shoe_invalid_penetration_greater_than_one():
    deck = Deck(number_of_decks=6, seed=42)
    
    with pytest.raises(ValueError, match="penetration must be between 0 and 1"):
        Shoe(deck, penetration=1.5)


def test_shoe_invalid_negative_variance():
    deck = Deck(number_of_decks=6, seed=42)
    
    with pytest.raises(ValueError, match="penetration_variance must be non-negative"):
        Shoe(deck, penetration=0.75, penetration_variance=-0.1)


# -------------------
# Representation
# -------------------

def test_shoe_str():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    s = str(shoe)
    assert "Shoe" in s
    assert "remaining=" in s
    assert "dealt=" in s
    assert "cut_card=" in s
    assert "needs_shuffle=" in s


def test_shoe_repr():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.05)
    
    r = repr(shoe)
    assert "Shoe" in r
    assert "cards_remaining=" in r
    assert "cards_dealt=" in r
    assert "cut_card_index=" in r
    assert "penetration=" in r
    assert "variance=" in r


# -------------------
# Cut card
# -------------------

def test_cut_card_index_calculated():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, seed=123)
    
    cut_card = shoe.cut_card_index()
    total_cards = 6 * 52
    
    # Cut card should be around 75% of total cards
    assert cut_card > 0
    assert cut_card < total_cards
    # Allow some tolerance for variance
    assert 0.6 * total_cards < cut_card < 0.9 * total_cards


def test_cut_card_with_zero_variance():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    expected = int(6 * 52 * 0.75)
    
    assert cut_card == expected


def test_cut_card_deterministic_with_seed():
    deck1 = Deck(number_of_decks=6, seed=42)
    deck2 = Deck(number_of_decks=6, seed=42)
    shoe1 = Shoe(deck1, penetration=0.75, penetration_variance=0.05, seed=123)
    shoe2 = Shoe(deck2, penetration=0.75, penetration_variance=0.05, seed=123)
    
    assert shoe1.cut_card_index() == shoe2.cut_card_index()


def test_cut_card_varies_with_different_seeds():
    deck1 = Deck(number_of_decks=6, seed=42)
    deck2 = Deck(number_of_decks=6, seed=42)
    shoe1 = Shoe(deck1, penetration=0.75, penetration_variance=0.05, seed=123)
    shoe2 = Shoe(deck2, penetration=0.75, penetration_variance=0.05, seed=456)
    
    # With variance, different seeds should produce different cut cards
    # (though there's a small chance they could be equal)
    assert shoe1.cut_card_index() != shoe2.cut_card_index()


def test_cut_card_clamped_to_valid_range():
    """Test that cut card is clamped even with high variance."""
    deck = Deck(number_of_decks=6, seed=42)
    # High variance might push penetration outside [0, 1]
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.5, seed=123)
    
    cut_card = shoe.cut_card_index()
    total_cards = 6 * 52
    
    # Should be clamped to valid range
    assert 0 <= cut_card <= total_cards


# -------------------
# Dealing
# -------------------

def test_shoe_deal_cards():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    cards = shoe.deal(5)
    
    assert len(cards) == 5
    assert all(isinstance(card, Card) for card in cards)
    assert shoe.num_cards_dealt() == 5
    assert shoe.num_cards_remaining() == 6 * 52 - 5
    assert_valid_dealing_device_state(shoe)


def test_shoe_next_card():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    card = shoe.next_card()
    
    assert isinstance(card, Card)
    assert shoe.num_cards_dealt() == 1
    assert shoe.num_cards_remaining() == 6 * 52 - 1
    assert_valid_dealing_device_state(shoe)


# -------------------
# Burning
# -------------------

def test_shoe_burn_adds_to_discard_tray():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    shoe.burn(3)
    
    assert shoe.num_cards_dealt() == 3
    assert len(shoe.discard_tray()) == 3
    assert_valid_dealing_device_state(shoe)


def test_shoe_burn_multiple_times():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    shoe.burn(2)
    shoe.burn(3)
    
    assert shoe.num_cards_dealt() == 5
    assert len(shoe.discard_tray()) == 5
    assert_valid_dealing_device_state(shoe)


# -------------------
# Discarding
# -------------------

def test_shoe_discard_single_card():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    card = shoe.next_card()
    shoe.discard(card)
    
    discard_tray = shoe.discard_tray()
    assert len(discard_tray) == 1
    assert discard_tray[0] == card


def test_shoe_discard_multiple_cards():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    cards = shoe.deal(5)
    shoe.discard(*cards)
    
    discard_tray = shoe.discard_tray()
    assert len(discard_tray) == 5
    assert discard_tray == cards


def test_shoe_discard_none_raises_error():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    with pytest.raises(ValueError, match="Cannot discard None"):
        shoe.discard(None)


def test_shoe_discard_tray_returns_copy():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    card = shoe.next_card()
    shoe.discard(card)
    
    tray1 = shoe.discard_tray()
    tray2 = shoe.discard_tray()
    
    # Should be equal but not the same object
    assert tray1 == tray2
    assert tray1 is not tray2


def test_shoe_discard_accumulates():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    card1 = shoe.next_card()
    shoe.discard(card1)
    assert len(shoe.discard_tray()) == 1
    
    card2 = shoe.next_card()
    shoe.discard(card2)
    assert len(shoe.discard_tray()) == 2
    
    cards = shoe.deal(3)
    shoe.discard(*cards)
    assert len(shoe.discard_tray()) == 5


# -------------------
# needs_shuffle
# -------------------

def test_shoe_needs_shuffle_false_initially():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    assert shoe.needs_shuffle() is False


def test_shoe_needs_shuffle_false_before_cut_card():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    shoe.deal(cut_card - 10)
    
    assert shoe.needs_shuffle() is False


def test_shoe_needs_shuffle_true_at_cut_card():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    shoe.deal(cut_card)
    
    assert shoe.needs_shuffle() is True


def test_shoe_needs_shuffle_true_after_cut_card():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    shoe.deal(cut_card + 10)
    
    assert shoe.needs_shuffle() is True


# -------------------
# Shuffling
# -------------------

def test_shoe_shuffle_resets_deck():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    shoe.deal(100)
    assert shoe.num_cards_dealt() == 100
    
    shoe.shuffle()
    
    assert shoe.num_cards_dealt() == 0
    assert shoe.num_cards_remaining() == 6 * 52
    assert_valid_dealing_device_state(shoe)


def test_shoe_shuffle_clears_discard_tray():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    cards = shoe.deal(10)
    shoe.discard(*cards)
    assert len(shoe.discard_tray()) == 10
    
    shoe.shuffle()
    
    assert len(shoe.discard_tray()) == 0


def test_shoe_shuffle_updates_cut_card():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.05, seed=123)
    
    cut_card_before = shoe.cut_card_index()
    shoe.shuffle()
    cut_card_after = shoe.cut_card_index()
    
    # With variance, cut card should change after shuffle
    # (though there's a small chance they could be equal)
    assert cut_card_before != cut_card_after


def test_shoe_shuffle_resets_needs_shuffle():
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    shoe.deal(cut_card)
    assert shoe.needs_shuffle() is True
    
    shoe.shuffle()
    
    assert shoe.needs_shuffle() is False


# -------------------
# Integration scenarios
# -------------------

def test_shoe_typical_game_flow():
    """Simulate a typical game flow with dealing, discarding, and shuffling."""
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    
    # Deal several hands
    for _ in range(10):
        cards = shoe.deal(5)
        shoe.discard(*cards)
    
    assert shoe.num_cards_dealt() == 50
    assert len(shoe.discard_tray()) == 50
    
    # Continue until cut card is reached
    while not shoe.needs_shuffle():
        cards = shoe.deal(5)
        shoe.discard(*cards)
    
    assert shoe.num_cards_dealt() >= cut_card
    assert shoe.needs_shuffle() is True
    
    # Shuffle
    shoe.shuffle()
    
    assert shoe.num_cards_dealt() == 0
    assert len(shoe.discard_tray()) == 0
    assert shoe.needs_shuffle() is False


def test_shoe_burn_and_discard_separate():
    """Test that burned cards and discarded cards both go to discard tray."""
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    # Burn some cards
    shoe.burn(3)
    assert len(shoe.discard_tray()) == 3
    
    # Deal and discard some cards
    cards = shoe.deal(5)
    shoe.discard(*cards)
    assert len(shoe.discard_tray()) == 8
    
    # Burn more cards
    shoe.burn(2)
    assert len(shoe.discard_tray()) == 10


def test_shoe_multiple_shuffle_cycles():
    """Test multiple shuffle cycles."""
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    for cycle in range(3):
        cut_card = shoe.cut_card_index()
        
        # Deal until cut card
        while not shoe.needs_shuffle():
            cards = shoe.deal(5)
            shoe.discard(*cards)
        
        assert shoe.needs_shuffle() is True
        
        # Shuffle for next cycle
        shoe.shuffle()
        
        assert shoe.needs_shuffle() is False
        assert shoe.num_cards_dealt() == 0
        assert len(shoe.discard_tray()) == 0


# -------------------
# Edge cases
# -------------------

def test_shoe_high_penetration():
    """Test shoe with very high penetration (close to 1.0)."""
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.99, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    total_cards = 6 * 52
    
    # Should be very close to total cards
    assert cut_card > 0.95 * total_cards
    assert cut_card < total_cards


def test_shoe_low_penetration():
    """Test shoe with very low penetration (close to 0.0)."""
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.01, penetration_variance=0.0)
    
    cut_card = shoe.cut_card_index()
    total_cards = 6 * 52
    
    # Should be very close to 0
    assert cut_card > 0
    assert cut_card < 0.05 * total_cards


def test_shoe_single_deck():
    """Test shoe with a single deck."""
    deck = Deck(number_of_decks=1, seed=42)
    shoe = Shoe(deck, penetration=0.75, penetration_variance=0.0)
    
    assert len(shoe) == 52
    cut_card = shoe.cut_card_index()
    assert cut_card == int(52 * 0.75)


# -------------------
# Invariants
# -------------------

def test_shoe_invariants_maintained():
    """Test that invariants are maintained throughout operations."""
    deck = Deck(number_of_decks=6, seed=42)
    shoe = Shoe(deck, penetration=0.75)
    
    # Initial state
    assert_valid_dealing_device_state(shoe)
    
    # After dealing
    shoe.deal(50)
    assert_valid_dealing_device_state(shoe)
    
    # After burning
    shoe.burn(10)
    assert_valid_dealing_device_state(shoe)
    
    # After shuffling
    shoe.shuffle()
    assert_valid_dealing_device_state(shoe)