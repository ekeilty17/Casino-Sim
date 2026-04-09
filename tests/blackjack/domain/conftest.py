"""Shared fixtures for blackjack domain tests."""
import pytest
from unittest.mock import Mock

from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import Player
from casino.blackjack.betting import BettingStrategy, FlatBettingStrategy
from casino.blackjack.decision import DecisionStrategy


@pytest.fixture
def ace_of_spades():
    """Ace of Spades card."""
    return Card(Rank.ACE, Suit.SPADE)


@pytest.fixture
def two_of_hearts():
    """Two of Hearts card."""
    return Card(Rank.TWO, Suit.HEART)


@pytest.fixture
def five_of_diamonds():
    """Five of Diamonds card."""
    return Card(Rank.FIVE, Suit.DIAMOND)


@pytest.fixture
def six_of_clubs():
    """Six of Clubs card."""
    return Card(Rank.SIX, Suit.CLUB)


@pytest.fixture
def ten_of_spades():
    """Ten of Spades card."""
    return Card(Rank.TEN, Suit.SPADE)


@pytest.fixture
def jack_of_hearts():
    """Jack of Hearts card."""
    return Card(Rank.JACK, Suit.HEART)


@pytest.fixture
def queen_of_diamonds():
    """Queen of Diamonds card."""
    return Card(Rank.QUEEN, Suit.DIAMOND)


@pytest.fixture
def king_of_clubs():
    """King of Clubs card."""
    return Card(Rank.KING, Suit.CLUB)


@pytest.fixture
def mock_decision_strategy():
    """Mock decision strategy."""
    return Mock(spec=DecisionStrategy)


@pytest.fixture
def mock_betting_strategy():
    """Mock betting strategy that returns a fixed bet."""
    strategy = Mock(spec=BettingStrategy)
    strategy.bet.return_value = 10
    return strategy


@pytest.fixture
def basic_player(mock_decision_strategy, mock_betting_strategy):
    """Create a basic player with $1000 bankroll."""
    return Player(
        player_id=1,
        name="Test Player",
        bankroll=1000,
        decision_strategy=mock_decision_strategy,
        betting_strategy=mock_betting_strategy
    )


@pytest.fixture
def poor_player(mock_decision_strategy, mock_betting_strategy):
    """Create a player with low bankroll ($50)."""
    return Player(
        player_id=2,
        name="Poor Player",
        bankroll=50,
        decision_strategy=mock_decision_strategy,
        betting_strategy=mock_betting_strategy
    )

# Made with Bob
