"""
Tests for Engine hand result determination.

Tests the hand_result method which determines the outcome of a player hand
against the dealer hand.
"""

import pytest

from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import PlayerHand, DealerHand, PlayerHandResult


def test_hand_result_player_surrendered(engine):
    """Test hand result when player surrenders."""
    player_hand = PlayerHand(bet=10, cards=[], is_surrendered=True)
    dealer_hand = DealerHand(cards=[Card(Rank.KING, Suit.SPADE)])
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.SURRENDERED


def test_hand_result_dealer_blackjack_with_peak(engine):
    """Test hand result when dealer has blackjack (with peak rule)."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.DIAMOND), Card(Rank.KING, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.LOSE


def test_hand_result_player_blackjack_with_peak(engine):
    """Test hand result when player has blackjack (with peak rule)."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.KING, Suit.DIAMOND), Card(Rank.QUEEN, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.WIN


def test_hand_result_both_blackjack_with_peak(engine):
    """Test hand result when both have blackjack (should be handled by peak logic)."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.DIAMOND), Card(Rank.KING, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    # Dealer blackjack is checked first, so player loses
    assert result == PlayerHandResult.LOSE


def test_hand_result_player_busted(engine):
    """Test hand result when player busts."""
    player_hand = PlayerHand(
        bet=10,
        cards=[
            Card(Rank.KING, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
            Card(Rank.FIVE, Suit.DIAMOND),
        ]
    )
    dealer_hand = DealerHand(cards=[Card(Rank.TEN, Suit.CLUB)])
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.LOSE


def test_hand_result_dealer_busted(engine):
    """Test hand result when dealer busts."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[
            Card(Rank.KING, Suit.DIAMOND),
            Card(Rank.QUEEN, Suit.CLUB),
            Card(Rank.FIVE, Suit.SPADE),
        ]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.WIN


def test_hand_result_push(engine):
    """Test hand result when player and dealer tie."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.KING, Suit.DIAMOND), Card(Rank.NINE, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.PUSH


def test_hand_result_player_wins(engine):
    """Test hand result when player has higher total."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.KING, Suit.DIAMOND), Card(Rank.EIGHT, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.WIN


def test_hand_result_dealer_wins(engine):
    """Test hand result when dealer has higher total."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.KING, Suit.DIAMOND), Card(Rank.NINE, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.LOSE


def test_hand_result_player_21_not_blackjack(engine):
    """Test hand result when player has 21 but not blackjack."""
    player_hand = PlayerHand(
        bet=10,
        cards=[
            Card(Rank.SEVEN, Suit.SPADE),
            Card(Rank.SEVEN, Suit.HEART),
            Card(Rank.SEVEN, Suit.DIAMOND),
        ]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.KING, Suit.CLUB), Card(Rank.NINE, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.WIN


def test_hand_result_split_hand_21_not_blackjack(engine):
    """Test that split hand with 21 is not treated as blackjack."""
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)],
        is_split=True,  # Split hands don't count as blackjack
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.KING, Suit.DIAMOND), Card(Rank.QUEEN, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    # Should be push (both 21), not win (blackjack beats 21)
    assert result == PlayerHandResult.PUSH


def test_hand_result_soft_hands(engine):
    """Test hand result with soft hands."""
    # Player soft 18 vs dealer hard 17
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.SEVEN, Suit.HEART)]
    )
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.DIAMOND), Card(Rank.SEVEN, Suit.CLUB)]
    )
    
    result = engine.hand_result(player_hand, dealer_hand)
    assert result == PlayerHandResult.WIN
