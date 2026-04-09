import pytest
from casino.domain import Deck, Card, Rank, Suit
from casino.dealing import ContinuousShuffleMachine
from casino.domain.deck import DeckExhaustedError

from .conftest import assert_valid_dealing_device_state


# -------------------
# Initialization
# -------------------

def test_csm_initialization():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    assert len(csm) == 6 * 52
    assert csm.num_cards_remaining() == 6 * 52
    assert csm.num_cards_dealt() == 0
    assert_valid_dealing_device_state(csm)


def test_csm_single_deck():
    deck = Deck(number_of_decks=1, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    assert len(csm) == 52
    assert csm.num_cards_remaining() == 52
    assert csm.num_cards_dealt() == 0
    assert_valid_dealing_device_state(csm)


def test_csm_multiple_decks():
    deck = Deck(number_of_decks=8, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    assert len(csm) == 8 * 52
    assert csm.num_cards_remaining() == 8 * 52
    assert csm.num_cards_dealt() == 0
    assert_valid_dealing_device_state(csm)


# -------------------
# Representation
# -------------------

def test_csm_str():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    s = str(csm)
    assert "ContinuousShuffleMachine" in s
    assert "Deck" in s


def test_csm_repr():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    r = repr(csm)
    assert "ContinuousShuffleMachine" in r
    assert "deck=" in r


# -------------------
# Dealing
# -------------------

def test_csm_deal_single_card():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    cards = csm.deal(1)
    
    assert len(cards) == 1
    assert isinstance(cards[0], Card)
    assert csm.num_cards_dealt() == 1
    assert csm.num_cards_remaining() == 6 * 52 - 1
    assert_valid_dealing_device_state(csm)


def test_csm_deal_multiple_cards():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    cards = csm.deal(10)
    
    assert len(cards) == 10
    assert all(isinstance(card, Card) for card in cards)
    assert csm.num_cards_dealt() == 10
    assert csm.num_cards_remaining() == 6 * 52 - 10
    assert_valid_dealing_device_state(csm)


def test_csm_next_card():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    card = csm.next_card()
    
    assert isinstance(card, Card)
    assert csm.num_cards_dealt() == 1
    assert csm.num_cards_remaining() == 6 * 52 - 1
    assert_valid_dealing_device_state(csm)


def test_csm_deal_exhaustion():
    deck = Deck(number_of_decks=1, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    csm.deal(52)
    
    with pytest.raises(DeckExhaustedError):
        csm.deal(1)


# -------------------
# Burning
# -------------------

def test_csm_burn_cards():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    csm.burn(5)
    
    assert csm.num_cards_dealt() == 5
    assert csm.num_cards_remaining() == 6 * 52 - 5
    assert_valid_dealing_device_state(csm)


def test_csm_burn_multiple_times():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    csm.burn(3)
    csm.burn(7)
    
    assert csm.num_cards_dealt() == 10
    assert csm.num_cards_remaining() == 6 * 52 - 10
    assert_valid_dealing_device_state(csm)


# -------------------
# Discarding
# -------------------

def test_csm_discard_is_noop():
    """Test that discard is a no-op in CSM."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    cards = csm.deal(5)
    
    # Discard should not raise an error
    csm.discard(*cards)
    
    # State should be unchanged (discard is a no-op)
    assert csm.num_cards_dealt() == 5
    assert_valid_dealing_device_state(csm)


def test_csm_discard_single_card():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    card = csm.next_card()
    
    # Should not raise an error
    csm.discard(card)
    
    assert csm.num_cards_dealt() == 1
    assert_valid_dealing_device_state(csm)


def test_csm_discard_multiple_cards():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    cards = csm.deal(10)
    
    # Should not raise an error
    csm.discard(*cards)
    
    assert csm.num_cards_dealt() == 10
    assert_valid_dealing_device_state(csm)


# -------------------
# needs_shuffle
# -------------------

def test_csm_needs_shuffle_always_true():
    """Test that CSM always needs shuffle (after each round)."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    # Should be true even initially
    assert csm.needs_shuffle() is True


def test_csm_needs_shuffle_after_dealing():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    csm.deal(50)
    
    # Should still be true
    assert csm.needs_shuffle() is True


def test_csm_needs_shuffle_after_shuffle():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    csm.shuffle()
    
    # Should still be true (always needs shuffle)
    assert csm.needs_shuffle() is True


# -------------------
# Shuffling
# -------------------

def test_csm_shuffle_resets_deck():
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    csm.deal(100)
    assert csm.num_cards_dealt() == 100
    
    csm.shuffle()
    
    assert csm.num_cards_dealt() == 0
    assert csm.num_cards_remaining() == 6 * 52
    assert_valid_dealing_device_state(csm)


def test_csm_shuffle_randomizes_deck():
    """Test that shuffle actually randomizes the deck."""
    deck1 = Deck(number_of_decks=1, seed=42)
    deck2 = Deck(number_of_decks=1, seed=42)
    csm1 = ContinuousShuffleMachine(deck1)
    csm2 = ContinuousShuffleMachine(deck2)
    
    # Get initial cards (unshuffled)
    initial_cards = csm1.deal(10)
    
    # Shuffle and deal from second CSM
    csm2.shuffle()
    shuffled_cards = csm2.deal(10)
    
    # Should be different (with high probability)
    assert initial_cards != shuffled_cards


def test_csm_shuffle_is_deterministic_with_seed():
    """Test that shuffle is deterministic with same seed."""
    deck1 = Deck(number_of_decks=6, seed=123)
    deck2 = Deck(number_of_decks=6, seed=123)
    csm1 = ContinuousShuffleMachine(deck1)
    csm2 = ContinuousShuffleMachine(deck2)
    
    csm1.shuffle()
    csm2.shuffle()
    
    cards1 = csm1.deal(20)
    cards2 = csm2.deal(20)
    
    assert cards1 == cards2


def test_csm_multiple_shuffles():
    """Test multiple shuffle cycles."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    for _ in range(5):
        csm.deal(50)
        csm.shuffle()
        
        assert csm.num_cards_dealt() == 0
        assert csm.num_cards_remaining() == 6 * 52
        assert_valid_dealing_device_state(csm)


# -------------------
# Integration scenarios
# -------------------

def test_csm_typical_game_flow():
    """Simulate a typical CSM game flow."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    # Play several rounds
    for round_num in range(10):
        # Deal a hand
        cards = csm.deal(5)
        
        # Discard (no-op in CSM)
        csm.discard(*cards)
        
        # Check if shuffle needed (always true for CSM)
        assert csm.needs_shuffle() is True
        
        # Shuffle after each round
        csm.shuffle()
        
        # Verify reset
        assert csm.num_cards_dealt() == 0
        assert csm.num_cards_remaining() == 6 * 52


def test_csm_continuous_play_without_exhaustion():
    """Test that CSM can play indefinitely with shuffles."""
    deck = Deck(number_of_decks=1, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    # Play many rounds, more than deck size
    for _ in range(100):
        # Deal some cards
        cards = csm.deal(5)
        
        # If getting low, shuffle
        if csm.num_cards_remaining() < 10:
            csm.shuffle()
        
        assert_valid_dealing_device_state(csm)


def test_csm_vs_shoe_behavior():
    """Compare CSM behavior to shoe - CSM always needs shuffle."""
    from casino.dealing import Shoe
    
    deck_csm = Deck(number_of_decks=6, seed=42)
    deck_shoe = Deck(number_of_decks=6, seed=42)
    
    csm = ContinuousShuffleMachine(deck_csm)
    shoe = Shoe(deck_shoe, penetration=0.75)
    
    # CSM always needs shuffle
    assert csm.needs_shuffle() is True
    
    # Shoe doesn't need shuffle initially
    assert shoe.needs_shuffle() is False
    
    # After dealing, CSM still needs shuffle
    csm.deal(10)
    assert csm.needs_shuffle() is True
    
    # Shoe still doesn't need shuffle (before cut card)
    shoe.deal(10)
    assert shoe.needs_shuffle() is False


# -------------------
# Edge cases
# -------------------

def test_csm_deal_all_cards_then_shuffle():
    """Test dealing all cards then shuffling."""
    deck = Deck(number_of_decks=1, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    # Deal all cards
    csm.deal(52)
    assert csm.num_cards_remaining() == 0
    
    # Shuffle should reset
    csm.shuffle()
    assert csm.num_cards_remaining() == 52
    assert csm.num_cards_dealt() == 0


def test_csm_shuffle_without_dealing():
    """Test shuffling without dealing any cards."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    # Shuffle immediately
    csm.shuffle()
    
    assert csm.num_cards_dealt() == 0
    assert csm.num_cards_remaining() == 6 * 52
    assert_valid_dealing_device_state(csm)


def test_csm_burn_then_shuffle():
    """Test burning cards then shuffling."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    csm.burn(20)
    assert csm.num_cards_dealt() == 20
    
    csm.shuffle()
    assert csm.num_cards_dealt() == 0
    assert csm.num_cards_remaining() == 6 * 52


# -------------------
# Invariants
# -------------------

def test_csm_invariants_maintained():
    """Test that invariants are maintained throughout operations."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    # Initial state
    assert_valid_dealing_device_state(csm)
    
    # After dealing
    csm.deal(50)
    assert_valid_dealing_device_state(csm)
    
    # After burning
    csm.burn(10)
    assert_valid_dealing_device_state(csm)
    
    # After discarding
    cards = csm.deal(5)
    csm.discard(*cards)
    assert_valid_dealing_device_state(csm)
    
    # After shuffling
    csm.shuffle()
    assert_valid_dealing_device_state(csm)


def test_csm_state_consistency_across_operations():
    """Test state consistency through various operations."""
    deck = Deck(number_of_decks=6, seed=42)
    csm = ContinuousShuffleMachine(deck)
    
    total_cards = 6 * 52
    
    # Deal some cards
    csm.deal(30)
    assert csm.num_cards_dealt() + csm.num_cards_remaining() == total_cards
    
    # Burn some cards
    csm.burn(20)
    assert csm.num_cards_dealt() + csm.num_cards_remaining() == total_cards
    
    # Shuffle
    csm.shuffle()
    assert csm.num_cards_dealt() + csm.num_cards_remaining() == total_cards
    assert csm.num_cards_dealt() == 0
    assert csm.num_cards_remaining() == total_cards