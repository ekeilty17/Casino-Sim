"""
Shared fixtures for blackjack engine tests.

This file contains pytest fixtures that are used across multiple test files.
"""

import pytest
from unittest.mock import Mock

from casino.domain import Card, Rank, Suit
from casino.dealing import DealingDevice
from casino.blackjack.engine import Engine
from casino.blackjack.domain import (
    Player,
    Limits,
    Rules,
    SurrenderRule,
    DoubleRule,
)
from casino.blackjack.betting import BettingStrategy
from casino.blackjack.decision import DecisionStrategy


# ============================================================================
# Dealing Device Fixtures
# ============================================================================

@pytest.fixture
def mock_dealing_device():
    """Create a mock dealing device with configurable card sequence."""
    device = Mock(spec=DealingDevice)
    return device


# ============================================================================
# Rules Fixtures
# ============================================================================

@pytest.fixture
def basic_rules():
    """Standard blackjack rules."""
    return Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=True,
        resplit_aces=True,
        hit_after_split_aces=True,
        surrender=SurrenderRule.LATE,
        dealer_peak=True,
        double=DoubleRule.ANY,
        max_splits=3,
    )


@pytest.fixture
def restrictive_rules():
    """More restrictive blackjack rules (European style)."""
    return Rules(
        dealer_hits_soft_17=True,
        blackjack_payout=1.5,
        double_after_split=False,
        resplit_aces=False,
        hit_after_split_aces=False,
        surrender=SurrenderRule.NEVER,
        dealer_peak=False,
        double=DoubleRule.SPECIFIC_TOTALS,
        double_allowed_totals=frozenset([9, 10, 11]),
        max_splits=1,
    )


@pytest.fixture
def no_peak_rules():
    """Rules without dealer peak (European style)."""
    return Rules(
        dealer_hits_soft_17=False,
        blackjack_payout=1.5,
        double_after_split=False,
        resplit_aces=False,
        hit_after_split_aces=False,
        surrender=SurrenderRule.NEVER,
        dealer_peak=False,
        double=DoubleRule.ANY,
    )


# ============================================================================
# Limits Fixtures
# ============================================================================

@pytest.fixture
def basic_limits():
    """Standard table limits."""
    return Limits(min_bet=10, max_bet=500)


@pytest.fixture
def high_stakes_limits():
    """High stakes table limits."""
    return Limits(min_bet=100, max_bet=10000)


# ============================================================================
# Strategy Fixtures
# ============================================================================

@pytest.fixture
def mock_betting_strategy():
    """Mock betting strategy that returns a fixed bet."""
    strategy = Mock(spec=BettingStrategy)
    strategy.bet.return_value = 10
    return strategy


@pytest.fixture
def mock_decision_strategy():
    """Mock decision strategy."""
    strategy = Mock(spec=DecisionStrategy)
    return strategy


# ============================================================================
# Player Fixtures
# ============================================================================

@pytest.fixture
def mock_player(mock_betting_strategy, mock_decision_strategy):
    """Create a mock player with sufficient bankroll."""
    return Player(
        player_id=1,
        name="Test Player",
        bankroll=1000,
        decision_strategy=mock_decision_strategy,
        betting_strategy=mock_betting_strategy,
    )


@pytest.fixture
def poor_player(mock_betting_strategy, mock_decision_strategy):
    """Create a player with low bankroll."""
    return Player(
        player_id=2,
        name="Poor Player",
        bankroll=5,
        decision_strategy=mock_decision_strategy,
        betting_strategy=mock_betting_strategy,
    )


@pytest.fixture
def rich_player(mock_betting_strategy, mock_decision_strategy):
    """Create a player with high bankroll."""
    return Player(
        player_id=3,
        name="Rich Player",
        bankroll=100000,
        decision_strategy=mock_decision_strategy,
        betting_strategy=mock_betting_strategy,
    )


# ============================================================================
# Engine Fixtures
# ============================================================================

@pytest.fixture
def engine(mock_dealing_device, mock_player, basic_rules, basic_limits):
    """Create a basic engine instance."""
    return Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )


@pytest.fixture
def restrictive_engine(mock_dealing_device, mock_player, restrictive_rules, basic_limits):
    """Create an engine with restrictive rules."""
    return Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=restrictive_rules,
        limits=basic_limits,
    )


# ============================================================================
# Card Fixtures
# ============================================================================

@pytest.fixture
def ace_spade():
    """Ace of Spades."""
    return Card(Rank.ACE, Suit.SPADE)


@pytest.fixture
def king_heart():
    """King of Hearts."""
    return Card(Rank.KING, Suit.HEART)


@pytest.fixture
def ten_diamond():
    """Ten of Diamonds."""
    return Card(Rank.TEN, Suit.DIAMOND)


@pytest.fixture
def nine_club():
    """Nine of Clubs."""
    return Card(Rank.NINE, Suit.CLUB)