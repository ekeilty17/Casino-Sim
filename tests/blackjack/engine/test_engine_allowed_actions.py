"""
Tests for Engine allowed actions logic.

Tests the get_allowed_actions method and related helper methods that determine
which actions are valid for a given hand based on game rules and context.
"""

import pytest

from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import Action, PlayerHand, Spot
from casino.blackjack.engine import Engine


def test_get_allowed_actions_basic(engine, mock_player):
    """Test basic allowed actions for a new hand."""
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    # Should allow hit, stand, double, surrender
    assert Action.HIT in actions
    assert Action.STAND in actions
    assert Action.DOUBLE in actions
    assert Action.SURRENDER in actions


def test_get_allowed_actions_can_split(engine, mock_player):
    """Test allowed actions when hand can be split."""
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    # Should allow split (K and Q both value 10)
    assert Action.SPLIT in actions


def test_get_allowed_actions_three_cards(engine, mock_player):
    """Test allowed actions with three cards (no double/split/surrender)."""
    hand = PlayerHand(
        bet=10,
        cards=[
            Card(Rank.FIVE, Suit.SPADE),
            Card(Rank.FOUR, Suit.HEART),
            Card(Rank.THREE, Suit.DIAMOND),
        ]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    # Should only allow hit and stand
    assert actions == {Action.HIT, Action.STAND}


def test_get_allowed_actions_no_surrender_rule(
    mock_dealing_device, mock_player, basic_limits
):
    """Test allowed actions when surrender is not allowed."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    
    rules = Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=True,
        hit_after_split_aces=True,
        surrender=SurrenderRule.NEVER,  # No surrender
        dealer_peak=True,
        double=DoubleRule.ANY,
    )
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=rules,
        limits=basic_limits,
    )
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    assert Action.SURRENDER not in actions


def test_get_allowed_actions_no_double_after_split(
    mock_dealing_device, mock_player, basic_limits
):
    """Test allowed actions when double after split is not allowed."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    
    rules = Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=False,  # No double after split
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
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)],
        is_split=True,
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    assert Action.DOUBLE not in actions


def test_get_allowed_actions_never_double(mock_dealing_device, mock_player, basic_limits):
    """Test allowed actions when doubling is never allowed."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    
    rules = Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=True,
        hit_after_split_aces=True,
        surrender=SurrenderRule.LATE,
        dealer_peak=True,
        double=DoubleRule.NEVER,  # Never allow double
    )
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=rules,
        limits=basic_limits,
    )
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    assert Action.DOUBLE not in actions


def test_get_allowed_actions_specific_totals_double(
    mock_dealing_device, mock_player, basic_limits
):
    """Test allowed actions with specific totals double rule."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    
    rules = Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=True,
        hit_after_split_aces=True,
        surrender=SurrenderRule.LATE,
        dealer_peak=True,
        double=DoubleRule.SPECIFIC_TOTALS,
        double_allowed_totals=frozenset([9, 10, 11]),
    )
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=rules,
        limits=basic_limits,
    )
    
    # Hand with total 11 (allowed)
    hand_allowed = PlayerHand(
        bet=10,
        cards=[Card(Rank.SIX, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand_allowed])
    actions = engine.get_allowed_actions(hand_allowed, spot)
    assert Action.DOUBLE in actions
    
    # Hand with total 12 (not allowed)
    hand_not_allowed = PlayerHand(
        bet=10,
        cards=[Card(Rank.SEVEN, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand_not_allowed])
    actions = engine.get_allowed_actions(hand_not_allowed, spot)
    assert Action.DOUBLE not in actions


def test_get_allowed_actions_insufficient_bankroll_double(engine, poor_player):
    """Test allowed actions when player lacks bankroll to double."""
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
    )
    spot = Spot(player=poor_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    assert Action.DOUBLE not in actions


def test_get_allowed_actions_insufficient_bankroll_split(engine, poor_player):
    """Test allowed actions when player lacks bankroll to split."""
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
    )
    spot = Spot(player=poor_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    assert Action.SPLIT not in actions


def test_get_allowed_actions_no_resplit_aces(
    mock_dealing_device, mock_player, basic_limits
):
    """Test allowed actions when resplit aces is not allowed."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    
    rules = Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=False,  # No resplit aces
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
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.ACE, Suit.HEART)],
        is_split=True,
        split_from_rank=Rank.ACE,
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    assert Action.SPLIT not in actions


def test_get_allowed_actions_max_splits_reached(
    mock_dealing_device, mock_player, basic_limits
):
    """Test allowed actions when max splits limit is reached."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    
    rules = Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=True,
        hit_after_split_aces=True,
        surrender=SurrenderRule.LATE,
        dealer_peak=True,
        double=DoubleRule.ANY,
        max_splits=2,  # Max 2 splits
    )
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=rules,
        limits=basic_limits,
    )
    
    # Create spot with 2 split hands already
    hand1 = PlayerHand(bet=10, cards=[Card(Rank.EIGHT, Suit.SPADE)], is_split=True)
    hand2 = PlayerHand(bet=10, cards=[Card(Rank.EIGHT, Suit.HEART)], is_split=True)
    hand3 = PlayerHand(
        bet=10,
        cards=[Card(Rank.EIGHT, Suit.DIAMOND), Card(Rank.EIGHT, Suit.CLUB)],
        is_split=False,
    )
    spot = Spot(player=mock_player, hands=[hand1, hand2, hand3])
    
    actions = engine.get_allowed_actions(hand3, spot)
    
    assert Action.SPLIT not in actions


def test_get_allowed_actions_no_hit_after_split_aces(
    mock_dealing_device, mock_player, basic_limits
):
    """Test allowed actions when hit after split aces is not allowed."""
    from casino.blackjack.domain import Rules, SurrenderRule, DoubleRule
    
    rules = Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=True,
        hit_after_split_aces=False,  # No hit after split aces
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
    
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.NINE, Suit.HEART)],
        is_split=True,
        split_from_rank=Rank.ACE,
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    # Should only allow stand
    assert actions == {Action.STAND}


def test_get_allowed_actions_pair_of_aces(engine, mock_player):
    """Test allowed actions with pair of aces."""
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.ACE, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    # Should allow split
    assert Action.SPLIT in actions


def test_get_allowed_actions_different_face_cards(engine, mock_player):
    """Test allowed actions with different face cards (same value)."""
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.JACK, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    # Should allow split (both value 10)
    assert Action.SPLIT in actions


def test_get_allowed_actions_ten_and_face_card(engine, mock_player):
    """Test allowed actions with 10 and face card."""
    hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
    )
    spot = Spot(player=mock_player, hands=[hand])
    
    actions = engine.get_allowed_actions(hand, spot)
    
    # Should allow split (both value 10)
    assert Action.SPLIT in actions