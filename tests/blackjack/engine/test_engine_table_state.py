"""
Tests for Engine table state initialization.

Tests the initialize_table_state method which sets up the initial game state.
"""

import pytest
from unittest.mock import Mock

from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import Player
from casino.blackjack.betting import BettingStrategy
from casino.blackjack.decision import DecisionStrategy


def test_initialize_table_state_single_player(engine, mock_dealing_device, mock_player):
    """Test table state initialization with one player."""
    # Setup dealing device to return cards
    cards = [
        Card(Rank.KING, Suit.SPADE),   # Player card 1
        Card(Rank.QUEEN, Suit.HEART),  # Player card 2
        Card(Rank.ACE, Suit.DIAMOND),  # Dealer card 1
        Card(Rank.TEN, Suit.CLUB),     # Dealer card 2
    ]
    mock_dealing_device.deal.side_effect = [cards[0:2], cards[2:4]]
    
    table_state = engine.initialize_table_state()
    
    # Verify player was asked to bet
    assert mock_player.betting_strategy.bet.called
    
    # Verify table state structure
    assert len(table_state.spots) == 1
    spot = table_state.spots[0]
    assert spot.player == mock_player
    assert len(spot.hands) == 1
    
    # Verify player hand
    hand = spot.hands[0]
    assert hand.bet == 10
    assert len(hand.cards) == 2
    assert hand.cards[0] == cards[0]
    assert hand.cards[1] == cards[1]
    
    # Verify dealer hand
    assert len(table_state.dealer_hand.cards) == 2
    assert table_state.dealer_hand.cards[0] == cards[2]
    assert table_state.dealer_hand.cards[1] == cards[3]


def test_initialize_table_state_multiple_players(
    mock_dealing_device, basic_rules, basic_limits
):
    """Test table state initialization with multiple players."""
    # Create multiple players
    players = []
    for i in range(3):
        betting_strategy = Mock(spec=BettingStrategy)
        betting_strategy.bet.return_value = 10 * (i + 1)
        decision_strategy = Mock(spec=DecisionStrategy)
        player = Player(
            player_id=i,
            name=f"Player {i}",
            bankroll=1000,
            decision_strategy=decision_strategy,
            betting_strategy=betting_strategy,
        )
        players.append(player)
    
    # Setup dealing device
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)],  # Player 0
        [Card(Rank.JACK, Suit.DIAMOND), Card(Rank.TEN, Suit.CLUB)],   # Player 1
        [Card(Rank.NINE, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)],  # Player 2
        [Card(Rank.ACE, Suit.DIAMOND), Card(Rank.KING, Suit.CLUB)],   # Dealer
    ]
    
    from casino.blackjack.engine import Engine
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=players,
        rules=basic_rules,
        limits=basic_limits,
    )
    
    table_state = engine.initialize_table_state()
    
    assert len(table_state.spots) == 3
    for i, spot in enumerate(table_state.spots):
        assert spot.player == players[i]
        assert len(spot.hands) == 1
        assert spot.hands[0].bet == 10 * (i + 1)


def test_initialize_table_state_player_not_betting(
    mock_dealing_device, basic_rules, basic_limits
):
    """Test table state when a player chooses not to bet."""
    betting_strategy = Mock(spec=BettingStrategy)
    betting_strategy.bet.return_value = 0  # Player sits out
    decision_strategy = Mock(spec=DecisionStrategy)
    
    player = Player(
        player_id=1,
        name="Sitting Out",
        bankroll=1000,
        decision_strategy=decision_strategy,
        betting_strategy=betting_strategy,
    )
    
    mock_dealing_device.deal.return_value = [
        Card(Rank.ACE, Suit.DIAMOND),
        Card(Rank.KING, Suit.CLUB),
    ]
    
    from casino.blackjack.engine import Engine
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    table_state = engine.initialize_table_state()
    
    # Player should have a spot but no hands
    assert len(table_state.spots) == 1
    assert table_state.spots[0].player == player
    assert len(table_state.spots[0].hands) == 0


def test_initialize_table_state_no_dealer_peak(
    mock_dealing_device, mock_player, no_peak_rules, basic_limits
):
    """Test table state initialization when dealer doesn't peak (European rules)."""
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)],  # Player
        [Card(Rank.ACE, Suit.DIAMOND)],  # Dealer gets only 1 card
    ]
    
    from casino.blackjack.engine import Engine
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=no_peak_rules,
        limits=basic_limits,
    )
    
    table_state = engine.initialize_table_state()
    
    # Dealer should have only 1 card
    assert len(table_state.dealer_hand.cards) == 1


def test_initialize_table_state_with_dealer_peak(engine, mock_dealing_device, mock_player):
    """Test table state initialization when dealer peaks (standard rules)."""
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)],  # Player
        [Card(Rank.ACE, Suit.DIAMOND), Card(Rank.KING, Suit.CLUB)],   # Dealer gets 2 cards
    ]
    
    table_state = engine.initialize_table_state()
    
    # Dealer should have 2 cards
    assert len(table_state.dealer_hand.cards) == 2


def test_initialize_table_state_mixed_betting(mock_dealing_device, basic_rules, basic_limits):
    """Test table state with some players betting and some not."""
    # Create players with different betting behaviors
    players = []
    for i in range(3):
        betting_strategy = Mock(spec=BettingStrategy)
        # Player 1 sits out (bet 0), others bet
        betting_strategy.bet.return_value = 0 if i == 1 else 10 * (i + 1)
        decision_strategy = Mock(spec=DecisionStrategy)
        player = Player(
            player_id=i,
            name=f"Player {i}",
            bankroll=1000,
            decision_strategy=decision_strategy,
            betting_strategy=betting_strategy,
        )
        players.append(player)
    
    # Setup dealing device - only 2 players betting
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.KING, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)],  # Player 0
        [Card(Rank.NINE, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)],  # Player 2
        [Card(Rank.ACE, Suit.DIAMOND), Card(Rank.KING, Suit.CLUB)],   # Dealer
    ]
    
    from casino.blackjack.engine import Engine
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=players,
        rules=basic_rules,
        limits=basic_limits,
    )
    
    table_state = engine.initialize_table_state()
    
    assert len(table_state.spots) == 3
    # Player 0 has hand
    assert len(table_state.spots[0].hands) == 1
    # Player 1 has no hands (sitting out)
    assert len(table_state.spots[1].hands) == 0
    # Player 2 has hand
    assert len(table_state.spots[2].hands) == 1

