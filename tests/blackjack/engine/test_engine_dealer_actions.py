"""
Tests for Engine dealer action handling.

Tests the dealer_action method which processes the dealer's turn according
to house rules.
"""

import pytest

from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import DealerHand, TableState


def test_dealer_action_hits_until_17(engine, mock_dealing_device):
    """Test dealer hits until reaching 17 or higher."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.SIX, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]  # Total 11
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    # Dealer will hit twice
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.FOUR, Suit.DIAMOND),  # Total 15
        Card(Rank.THREE, Suit.CLUB),    # Total 18
    ]
    
    engine.dealer_action(table_state)
    
    assert len(dealer_hand.cards) == 4
    assert dealer_hand.get_total() == 18


def test_dealer_action_stands_on_17(engine, mock_dealing_device):
    """Test dealer stands on 17."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.SEVEN, Suit.HEART)]  # Total 17
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    engine.dealer_action(table_state)
    
    # Dealer should not hit
    assert len(dealer_hand.cards) == 2
    assert not mock_dealing_device.next_card.called


def test_dealer_action_stands_on_hard_17(engine, mock_dealing_device):
    """Test dealer stands on hard 17."""
    dealer_hand = DealerHand(
        cards=[
            Card(Rank.TEN, Suit.SPADE),
            Card(Rank.FIVE, Suit.HEART),
            Card(Rank.TWO, Suit.DIAMOND),
        ]  # Total 17
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    engine.dealer_action(table_state)
    
    # Dealer should not hit
    assert len(dealer_hand.cards) == 3
    assert not mock_dealing_device.next_card.called


def test_dealer_action_stands_on_soft_17_when_rule_false(engine, mock_dealing_device):
    """Test dealer stands on soft 17 when dealer_hits_soft_17 is False."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.SIX, Suit.HEART)]  # Soft 17
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    # Engine has dealer_hits_soft_17=False by default
    engine.dealer_action(table_state)
    
    # Dealer should not hit
    assert len(dealer_hand.cards) == 2
    assert not mock_dealing_device.next_card.called


def test_dealer_action_hits_soft_17_when_rule_true(
    mock_dealing_device, mock_player, basic_limits
):
    """Test dealer hits on soft 17 when dealer_hits_soft_17 is True."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    from casino.blackjack.engine import Engine
    
    rules = Rules(
        dealer_hits_soft_17=True,  # Dealer hits soft 17
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=True,
        hit_after_split_aces=True,
        surrender=SurrenderRule.LATE,
        dealer_peak=True,
        double=DoubleRule.ANY,
    )
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=rules,
        limits=basic_limits,
    )
    
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.SIX, Suit.HEART)]  # Soft 17
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    mock_dealing_device.next_card.return_value = Card(Rank.FOUR, Suit.DIAMOND)
    
    engine.dealer_action(table_state)
    
    # Dealer should have hit
    assert len(dealer_hand.cards) == 3


def test_dealer_action_busts(engine, mock_dealing_device):
    """Test dealer busts."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]  # Total 19
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    mock_dealing_device.next_card.return_value = Card(Rank.FIVE, Suit.DIAMOND)
    
    engine.dealer_action(table_state)
    
    # Dealer should have busted
    assert dealer_hand.is_busted()
    assert dealer_hand.get_total() > 21


def test_dealer_action_stands_on_18(engine, mock_dealing_device):
    """Test dealer stands on 18."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)]  # Total 18
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    engine.dealer_action(table_state)
    
    # Dealer should not hit
    assert len(dealer_hand.cards) == 2
    assert not mock_dealing_device.next_card.called


def test_dealer_action_stands_on_19(engine, mock_dealing_device):
    """Test dealer stands on 19."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]  # Total 19
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    engine.dealer_action(table_state)
    
    # Dealer should not hit
    assert len(dealer_hand.cards) == 2
    assert not mock_dealing_device.next_card.called


def test_dealer_action_stands_on_20(engine, mock_dealing_device):
    """Test dealer stands on 20."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.KING, Suit.HEART)]  # Total 20
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    engine.dealer_action(table_state)
    
    # Dealer should not hit
    assert len(dealer_hand.cards) == 2
    assert not mock_dealing_device.next_card.called


def test_dealer_action_stands_on_21(engine, mock_dealing_device):
    """Test dealer stands on 21."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]  # Total 21
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    engine.dealer_action(table_state)
    
    # Dealer should not hit
    assert len(dealer_hand.cards) == 2
    assert not mock_dealing_device.next_card.called


def test_dealer_action_hits_on_16(engine, mock_dealing_device):
    """Test dealer hits on 16."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.SIX, Suit.HEART)]  # Total 16
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    mock_dealing_device.next_card.return_value = Card(Rank.FIVE, Suit.DIAMOND)
    
    engine.dealer_action(table_state)
    
    # Dealer should have hit
    assert len(dealer_hand.cards) == 3


def test_dealer_action_soft_hand_becomes_hard(engine, mock_dealing_device):
    """Test dealer with soft hand that becomes hard."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]  # Soft 16
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    # Dealer hits and gets a card that makes it hard
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.KING, Suit.DIAMOND),  # Now hard 16 (A=1, 5, K)
        Card(Rank.FIVE, Suit.CLUB),     # Now 21
    ]
    
    engine.dealer_action(table_state)
    
    # Dealer should have hit twice
    assert len(dealer_hand.cards) == 4
    assert dealer_hand.get_total() == 21


def test_dealer_action_multiple_hits(engine, mock_dealing_device):
    """Test dealer hitting multiple times."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.TWO, Suit.SPADE), Card(Rank.THREE, Suit.HEART)]  # Total 5
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.TWO, Suit.DIAMOND),   # Total 7
        Card(Rank.THREE, Suit.CLUB),    # Total 10
        Card(Rank.FOUR, Suit.SPADE),    # Total 14
        Card(Rank.FIVE, Suit.HEART),    # Total 19
    ]
    
    engine.dealer_action(table_state)
    
    # Dealer should have hit 4 times
    assert len(dealer_hand.cards) == 6
    assert dealer_hand.get_total() == 19


def test_dealer_action_with_soft_18(engine, mock_dealing_device):
    """Test dealer with soft 18 (should stand)."""
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.SEVEN, Suit.HEART)]  # Soft 18
    )
    table_state = TableState(dealer_hand=dealer_hand, spots=[])
    
    engine.dealer_action(table_state)
    
    # Dealer should not hit (soft 18 >= 17)
    assert len(dealer_hand.cards) == 2
    assert not mock_dealing_device.next_card.called
