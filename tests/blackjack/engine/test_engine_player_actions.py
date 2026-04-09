"""
Tests for Engine player action handling.

Tests the player_action method which processes player decisions and updates
game state accordingly.
"""

import pytest
from unittest.mock import Mock

from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import Action, PlayerHand, DealerHand, Spot


def test_player_action_stand(engine, mock_dealing_device, mock_player):
    """Test player action when choosing to stand."""
    mock_player.decision_strategy.decide.return_value = Action.STAND
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    assert not hand.is_active


def test_player_action_hit(engine, mock_dealing_device, mock_player):
    """Test player action when choosing to hit."""
    mock_player.decision_strategy.decide.side_effect = [Action.HIT, Action.STAND]
    mock_dealing_device.next_card.return_value = Card(Rank.FIVE, Suit.DIAMOND)
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    assert len(hand.cards) == 3
    assert hand.cards[2] == Card(Rank.FIVE, Suit.DIAMOND)


def test_player_action_hit_multiple_times(engine, mock_dealing_device, mock_player):
    """Test player action when hitting multiple times."""
    mock_player.decision_strategy.decide.side_effect = [
        Action.HIT,
        Action.HIT,
        Action.STAND
    ]
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.TWO, Suit.DIAMOND),
        Card(Rank.THREE, Suit.CLUB),
    ]
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.FIVE, Suit.SPADE), Card(Rank.FOUR, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    assert len(hand.cards) == 4
    assert not hand.is_active


def test_player_action_surrender(engine, mock_dealing_device, mock_player):
    """Test player action when choosing to surrender."""
    mock_player.decision_strategy.decide.return_value = Action.SURRENDER
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.SIX, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    assert not hand.is_active
    assert hand.is_surrendered


def test_player_action_double(engine, mock_dealing_device, mock_player):
    """Test player action when choosing to double."""
    mock_player.decision_strategy.decide.return_value = Action.DOUBLE
    mock_dealing_device.next_card.return_value = Card(Rank.FIVE, Suit.DIAMOND)
    
    initial_bankroll = mock_player.bankroll
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.SIX, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    assert not hand.is_active
    assert hand.is_doubled
    assert len(hand.cards) == 3
    assert mock_player.bankroll == initial_bankroll - 10  # Additional bet deducted


def test_player_action_double_insufficient_bankroll(engine, mock_dealing_device, poor_player):
    """Test player action double with insufficient bankroll raises error."""
    poor_player.decision_strategy.decide.return_value = Action.DOUBLE
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.SIX, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]
    )
    spot = Spot(player=poor_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    with pytest.raises(ValueError, match="Cannot double hand"):
        engine.player_action(spot, dealer_hand)


def test_player_action_split(engine, mock_dealing_device, mock_player):
    """Test player action when choosing to split."""
    mock_player.decision_strategy.decide.side_effect = [
        Action.SPLIT,
        Action.STAND,
        Action.STAND,
    ]
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.NINE, Suit.DIAMOND),
        Card(Rank.EIGHT, Suit.CLUB),
    ]
    
    initial_bankroll = mock_player.bankroll
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    # Should have 2 hands now
    assert len(spot.hands) == 2
    assert all(h.is_split for h in spot.hands)
    assert mock_player.bankroll == initial_bankroll - 10  # Additional bet deducted


def test_player_action_split_then_hit(engine, mock_dealing_device, mock_player):
    """Test player action when splitting then hitting on one hand."""
    mock_player.decision_strategy.decide.side_effect = [
        Action.SPLIT,
        Action.HIT,
        Action.STAND,
        Action.STAND,
    ]
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.NINE, Suit.DIAMOND),  # Second card for first split hand
        Card(Rank.EIGHT, Suit.CLUB),    # Second card for second split hand
        Card(Rank.TWO, Suit.SPADE),     # Hit on first hand
    ]
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.EIGHT, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    # Should have 2 hands
    assert len(spot.hands) == 2
    # First hand should have 3 cards (hit once)
    assert len(spot.hands[0].cards) == 3
    # Second hand should have 2 cards (stood)
    assert len(spot.hands[1].cards) == 2


def test_player_action_hand_with_one_card(engine, mock_dealing_device, mock_player):
    """Test player action deals card to hand with only one card (from split)."""
    mock_player.decision_strategy.decide.return_value = Action.STAND
    mock_dealing_device.next_card.return_value = Card(Rank.NINE, Suit.DIAMOND)
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE)],  # Only one card
        is_split=True,
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    # Should have received second card
    assert len(hand.cards) == 2


def test_player_action_empty_hand_raises_error(engine, mock_dealing_device, mock_player):
    """Test player action with empty hand raises error."""
    hand = PlayerHand(bet=10, cards=[])  # Empty hand
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    with pytest.raises(ValueError, match="Unexpected hand length of 0"):
        engine.player_action(spot, dealer_hand)


def test_player_action_only_one_action_available(engine, mock_dealing_device, mock_player):
    """Test player action when only one action is available (auto-selected)."""
    from unittest.mock import patch
    
    # Hand with 3 cards can only hit or stand
    hand = PlayerHand(
        bet=10,
        cards=[
            Card(Rank.KING, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
            Card(Rank.ACE, Suit.DIAMOND),  # Total 21
        ]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.CLUB)])
    
    # Mock to return only STAND action
    with patch.object(engine, 'get_allowed_actions', return_value={Action.STAND}):
        engine.player_action(spot, dealer_hand)
    
    # Decision strategy should not be called when only one action
    assert not mock_player.decision_strategy.decide.called
    assert not hand.is_active


def test_player_action_busts_automatically(engine, mock_dealing_device, mock_player):
    """Test player action when hitting causes bust."""
    mock_player.decision_strategy.decide.return_value = Action.HIT
    mock_dealing_device.next_card.return_value = Card(Rank.KING, Suit.DIAMOND)
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    # Hand should be busted
    assert hand.is_busted()
    assert len(hand.cards) == 3


def test_player_action_multiple_hands_in_spot(engine, mock_dealing_device, mock_player):
    """Test player action processes all hands in a spot."""
    mock_player.decision_strategy.decide.side_effect = [
        Action.STAND,
        Action.STAND,
    ]
    
    hand1 = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    hand2 = PlayerHand(
        bet=10,
        cards=[Card(Rank.QUEEN, Suit.DIAMOND), Card(Rank.EIGHT, Suit.CLUB)]
    )
    spot = Spot(player=mock_player, hands=[hand1, hand2])
    dealer_hand = DealerHand(cards=[Card(Rank.ACE, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    # Both hands should be inactive
    assert not hand1.is_active
    assert not hand2.is_active


def test_player_action_decision_context_passed_correctly(engine, mock_dealing_device, mock_player):
    """Test that decision context is passed correctly to strategy."""
    mock_player.decision_strategy.decide.return_value = Action.STAND
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_upcard = Card(Rank.ACE, Suit.DIAMOND)
    dealer_hand = DealerHand(cards=[dealer_upcard])
    
    engine.player_action(spot, dealer_hand)
    
    # Verify decision strategy was called with correct context
    assert mock_player.decision_strategy.decide.called
    call_args = mock_player.decision_strategy.decide.call_args[0][0]
    assert call_args.dealer_upcard == dealer_upcard
    assert call_args.hand == hand
    assert call_args.dealer_hits_soft_17 == engine.rules.dealer_hits_soft_17


def test_player_action_resplit_aces(engine, mock_dealing_device, mock_player):
    """Test player action when resplitting aces."""
    mock_player.decision_strategy.decide.side_effect = [
        Action.SPLIT,  # Split first pair
        Action.SPLIT,  # Split again (resplit)
        Action.STAND,
        Action.STAND,
        Action.STAND,
    ]
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.ACE, Suit.DIAMOND),  # Second card for first hand (another ace!)
        Card(Rank.NINE, Suit.CLUB),    # Second card for second hand
        Card(Rank.EIGHT, Suit.SPADE),  # Second card for third hand (from resplit)
        Card(Rank.SEVEN, Suit.HEART),  # Second card for fourth hand (from resplit)
    ]
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.ACE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    dealer_hand = DealerHand(cards=[Card(Rank.TEN, Suit.DIAMOND)])
    
    engine.player_action(spot, dealer_hand)
    
    # Should have 3 hands after resplit
    assert len(spot.hands) == 3

