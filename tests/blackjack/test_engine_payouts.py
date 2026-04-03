"""
Tests for Engine payout logic.

Tests the payout method which handles player winnings based on hand results.
"""

import pytest

from casino.blackjack.domain import PlayerHandResult


def test_payout_win(mock_player, engine):
    """Test payout for winning hand."""
    initial_bankroll = mock_player.bankroll
    engine.payout(mock_player, bet=100, result=PlayerHandResult.WIN)
    
    # Player should receive 2x bet
    assert mock_player.bankroll == initial_bankroll + 200


def test_payout_push(mock_player, engine):
    """Test payout for push."""
    initial_bankroll = mock_player.bankroll
    engine.payout(mock_player, bet=100, result=PlayerHandResult.PUSH)
    
    # Player should receive bet back
    assert mock_player.bankroll == initial_bankroll + 100


def test_payout_lose(mock_player, engine):
    """Test payout for losing hand."""
    initial_bankroll = mock_player.bankroll
    engine.payout(mock_player, bet=100, result=PlayerHandResult.LOSE)
    
    # Player should receive nothing
    assert mock_player.bankroll == initial_bankroll


def test_payout_surrendered(mock_player, engine):
    """Test payout for surrendered hand."""
    initial_bankroll = mock_player.bankroll
    engine.payout(mock_player, bet=100, result=PlayerHandResult.SURRENDERED)
    
    # Player should receive half bet back
    assert mock_player.bankroll == initial_bankroll + 50


def test_payout_surrendered_odd_bet(mock_player, engine):
    """Test payout for surrendered hand with odd bet amount."""
    initial_bankroll = mock_player.bankroll
    engine.payout(mock_player, bet=15, result=PlayerHandResult.SURRENDERED)
    
    # Player should receive half bet back (integer division)
    assert mock_player.bankroll == initial_bankroll + 7


def test_payout_multiple_wins(mock_player, engine):
    """Test multiple winning payouts accumulate correctly."""
    initial_bankroll = mock_player.bankroll
    
    engine.payout(mock_player, bet=10, result=PlayerHandResult.WIN)
    engine.payout(mock_player, bet=20, result=PlayerHandResult.WIN)
    engine.payout(mock_player, bet=30, result=PlayerHandResult.WIN)
    
    # Total payout: 20 + 40 + 60 = 120
    assert mock_player.bankroll == initial_bankroll + 120


def test_payout_mixed_results(mock_player, engine):
    """Test payouts with mixed results."""
    initial_bankroll = mock_player.bankroll
    
    engine.payout(mock_player, bet=10, result=PlayerHandResult.WIN)      # +20
    engine.payout(mock_player, bet=10, result=PlayerHandResult.LOSE)     # +0
    engine.payout(mock_player, bet=10, result=PlayerHandResult.PUSH)     # +10
    engine.payout(mock_player, bet=10, result=PlayerHandResult.SURRENDERED)  # +5
    
    # Total payout: 20 + 0 + 10 + 5 = 35
    assert mock_player.bankroll == initial_bankroll + 35


def test_payout_large_bet_win(rich_player, engine):
    """Test payout for large winning bet."""
    initial_bankroll = rich_player.bankroll
    engine.payout(rich_player, bet=5000, result=PlayerHandResult.WIN)
    
    # Player should receive 2x bet
    assert rich_player.bankroll == initial_bankroll + 10000


def test_payout_minimum_bet(mock_player, engine):
    """Test payout with minimum bet."""
    initial_bankroll = mock_player.bankroll
    engine.payout(mock_player, bet=1, result=PlayerHandResult.WIN)
    
    # Player should receive 2x bet
    assert mock_player.bankroll == initial_bankroll + 2


def test_compare_and_payout_hands_single_hand(engine, mock_player):
    """Test compare and payout for a single hand."""
    from casino.domain import Card, Rank, Suit
    from casino.blackjack.domain import DealerHand, PlayerHand, Spot, TableState
    
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)]
    )
    
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.DIAMOND), Card(Rank.NINE, Suit.CLUB)]
    )
    
    spot = Spot(player=mock_player, hands=[player_hand])
    table_state = TableState(dealer_hand=dealer_hand, spots=[spot])
    
    initial_bankroll = mock_player.bankroll
    
    engine.compare_and_payout_hands(table_state)
    
    # Player wins (19 vs 18): +20
    assert mock_player.bankroll == initial_bankroll + 20


def test_compare_and_payout_hands_multiple_hands(engine, mock_player):
    """Test compare and payout for multiple hands."""
    from casino.domain import Card, Rank, Suit
    from casino.blackjack.domain import DealerHand, PlayerHand, Spot, TableState
    
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)]
    )
    
    # Create multiple hands with different outcomes
    hand1 = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.DIAMOND), Card(Rank.NINE, Suit.CLUB)]
    )  # Win (19 vs 18)
    hand2 = PlayerHand(
        bet=20,
        cards=[Card(Rank.TEN, Suit.HEART), Card(Rank.EIGHT, Suit.DIAMOND)]
    )  # Push (18 vs 18)
    hand3 = PlayerHand(
        bet=30,
        cards=[Card(Rank.TEN, Suit.CLUB), Card(Rank.SEVEN, Suit.SPADE)]
    )  # Lose (17 vs 18)
    
    spot = Spot(player=mock_player, hands=[hand1, hand2, hand3])
    table_state = TableState(dealer_hand=dealer_hand, spots=[spot])
    
    initial_bankroll = mock_player.bankroll
    
    engine.compare_and_payout_hands(table_state)
    
    # hand1 wins: +20, hand2 pushes: +20, hand3 loses: +0
    expected_bankroll = initial_bankroll + 20 + 20 + 0
    assert mock_player.bankroll == expected_bankroll


def test_compare_and_payout_hands_multiple_players(engine, mock_dealing_device, basic_rules, basic_limits):
    """Test compare and payout for multiple players."""
    from unittest.mock import Mock
    from casino.domain import Card, Rank, Suit
    from casino.blackjack.domain import Player, DealerHand, PlayerHand, Spot, TableState
    from casino.blackjack.betting import BettingStrategy
    from casino.blackjack.decision import DecisionStrategy
    from casino.blackjack.engine import Engine
    
    # Create multiple players
    players = []
    for i in range(3):
        betting_strategy = Mock(spec=BettingStrategy)
        decision_strategy = Mock(spec=DecisionStrategy)
        player = Player(
            player_id=i,
            name=f"Player {i}",
            bankroll=1000,
            decision_strategy=decision_strategy,
            betting_strategy=betting_strategy,
        )
        players.append(player)
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=players,
        rules=basic_rules,
        limits=basic_limits,
    )
    
    dealer_hand = DealerHand(
        cards=[Card(Rank.TEN, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)]
    )
    
    # Player 0 wins
    hand0 = PlayerHand(bet=10, cards=[Card(Rank.TEN, Suit.DIAMOND), Card(Rank.NINE, Suit.CLUB)])
    spot0 = Spot(player=players[0], hands=[hand0])
    
    # Player 1 pushes
    hand1 = PlayerHand(bet=20, cards=[Card(Rank.TEN, Suit.HEART), Card(Rank.EIGHT, Suit.DIAMOND)])
    spot1 = Spot(player=players[1], hands=[hand1])
    
    # Player 2 loses
    hand2 = PlayerHand(bet=30, cards=[Card(Rank.TEN, Suit.CLUB), Card(Rank.SEVEN, Suit.SPADE)])
    spot2 = Spot(player=players[2], hands=[hand2])
    
    table_state = TableState(dealer_hand=dealer_hand, spots=[spot0, spot1, spot2])
    
    initial_bankrolls = [p.bankroll for p in players]
    
    engine.compare_and_payout_hands(table_state)
    
    # Player 0 wins: +20
    assert players[0].bankroll == initial_bankrolls[0] + 20
    # Player 1 pushes: +20
    assert players[1].bankroll == initial_bankrolls[1] + 20
    # Player 2 loses: +0
    assert players[2].bankroll == initial_bankrolls[2] + 0
