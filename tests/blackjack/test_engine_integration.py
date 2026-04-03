"""
Integration tests for Engine.

Tests complete game flows from initialization through payout, ensuring all
components work together correctly.
"""

import pytest

from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import Action
from casino.blackjack.engine import Engine


def test_run_round_dealer_blackjack_with_peak(engine, mock_dealing_device, mock_player):
    """Test run round when dealer has blackjack with peak rule."""
    from casino.blackjack.domain import DealerHand, PlayerHand, Spot, TableState
    
    dealer_hand = DealerHand(
        cards=[Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
    )
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.DIAMOND), Card(Rank.NINE, Suit.CLUB)]
    )
    spot = Spot(player=mock_player, hands=[player_hand])
    table_state = TableState(dealer_hand=dealer_hand, spots=[spot])
    
    initial_bankroll = mock_player.bankroll
    
    engine.run_round(table_state)
    
    # Player should not have been asked for actions
    assert not mock_player.decision_strategy.decide.called
    
    # Player should lose bet
    assert mock_player.bankroll == initial_bankroll


def test_run_round_complete_game(engine, mock_dealing_device, mock_player):
    """Test complete round from start to finish."""
    from casino.blackjack.domain import DealerHand, PlayerHand, Spot, TableState
    
    mock_player.decision_strategy.decide.return_value = Action.STAND
    
    dealer_hand = DealerHand(
        cards=[Card(Rank.SIX, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]
    )
    player_hand = PlayerHand(
        bet=10,
        cards=[Card(Rank.TEN, Suit.DIAMOND), Card(Rank.NINE, Suit.CLUB)]
    )
    spot = Spot(player=mock_player, hands=[player_hand])
    table_state = TableState(dealer_hand=dealer_hand, spots=[spot])
    
    # Dealer will hit and bust
    mock_dealing_device.next_card.return_value = Card(Rank.KING, Suit.DIAMOND)
    
    initial_bankroll = mock_player.bankroll
    
    engine.run_round(table_state)
    
    # Dealer hole card should be revealed
    assert dealer_hand.hole_card_revealed
    
    # Player should win (dealer busted)
    assert mock_player.bankroll == initial_bankroll + 20


def test_run_full_game_integration(mock_dealing_device, mock_player, basic_rules, basic_limits):
    """Integration test for a complete game from initialization to payout."""
    # Setup cards for initial deal
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)],  # Player
        [Card(Rank.SIX, Suit.DIAMOND), Card(Rank.FIVE, Suit.CLUB)],  # Dealer
    ]
    
    # Player will hit once then stand
    mock_player.decision_strategy.decide.side_effect = [Action.HIT, Action.STAND]
    
    # Cards for player hit and dealer hits
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.ACE, Suit.DIAMOND),  # Player hits (total 20)
        Card(Rank.FOUR, Suit.SPADE),   # Dealer hits (total 15)
        Card(Rank.THREE, Suit.HEART),  # Dealer hits (total 18)
    ]
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    initial_bankroll = mock_player.bankroll
    
    engine.run()
    
    # Player should win (20 vs 18)
    assert mock_player.bankroll == initial_bankroll - 10 + 20  # Bet 10, win 20


def test_run_full_game_player_busts(mock_dealing_device, mock_player, basic_rules, basic_limits):
    """Integration test where player busts."""
    # Setup cards for initial deal
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)],  # Player (19)
        [Card(Rank.SIX, Suit.DIAMOND), Card(Rank.FIVE, Suit.CLUB)],  # Dealer (11)
    ]
    
    # Player will hit and bust
    mock_player.decision_strategy.decide.return_value = Action.HIT
    
    # Player hits and busts
    mock_dealing_device.next_card.return_value = Card(Rank.KING, Suit.DIAMOND)  # Total 29
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    initial_bankroll = mock_player.bankroll
    
    engine.run()
    
    # Player should lose (busted)
    assert mock_player.bankroll == initial_bankroll - 10  # Lost bet


def test_run_full_game_player_doubles_and_wins(
    mock_dealing_device, mock_player, basic_rules, basic_limits
):
    """Integration test where player doubles down and wins."""
    # Setup cards for initial deal
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.SIX, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)],  # Player (11)
        [Card(Rank.SIX, Suit.DIAMOND), Card(Rank.FIVE, Suit.CLUB)],  # Dealer (11)
    ]
    
    # Player will double
    mock_player.decision_strategy.decide.return_value = Action.DOUBLE
    
    # Cards for double and dealer hits
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.NINE, Suit.DIAMOND),  # Player doubles (total 20)
        Card(Rank.FOUR, Suit.SPADE),    # Dealer hits (total 15)
        Card(Rank.THREE, Suit.HEART),   # Dealer hits (total 18)
    ]
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    initial_bankroll = mock_player.bankroll
    
    engine.run()
    
    # Player should win with doubled bet (20 vs 18)
    # Bet 10, doubled to 20, win 40
    assert mock_player.bankroll == initial_bankroll - 20 + 40


def test_run_full_game_player_splits_and_wins_both(
    mock_dealing_device, mock_player, basic_rules, basic_limits
):
    """Integration test where player splits and wins both hands."""
    # Setup cards for initial deal
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.EIGHT, Suit.SPADE), Card(Rank.EIGHT, Suit.HEART)],  # Player (pair)
        [Card(Rank.SIX, Suit.DIAMOND), Card(Rank.FIVE, Suit.CLUB)],    # Dealer (11)
    ]
    
    # Player will split then stand on both hands
    mock_player.decision_strategy.decide.side_effect = [
        Action.SPLIT,
        Action.STAND,
        Action.STAND,
    ]
    
    # Cards for split hands and dealer
    mock_dealing_device.next_card.side_effect = [
        Card(Rank.TEN, Suit.DIAMOND),  # First split hand (total 18)
        Card(Rank.NINE, Suit.CLUB),    # Second split hand (total 17)
        Card(Rank.FOUR, Suit.SPADE),   # Dealer hits (total 15)
        Card(Rank.ACE, Suit.HEART),    # Dealer hits (total 16)
    ]
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    initial_bankroll = mock_player.bankroll
    
    engine.run()
    
    # Player should win both hands (18 vs 16, 17 vs 16)
    # Bet 10 on each hand (20 total), win 40 total
    assert mock_player.bankroll == initial_bankroll - 20 + 40


def test_run_full_game_player_surrenders(
    mock_dealing_device, mock_player, basic_rules, basic_limits
):
    """Integration test where player surrenders."""
    # Setup cards for initial deal
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.TEN, Suit.SPADE), Card(Rank.SIX, Suit.HEART)],  # Player (16)
        [Card(Rank.ACE, Suit.DIAMOND), Card(Rank.FIVE, Suit.CLUB)],  # Dealer (soft 16)
    ]
    
    # Player will surrender
    mock_player.decision_strategy.decide.return_value = Action.SURRENDER
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    initial_bankroll = mock_player.bankroll
    
    engine.run()
    
    # Player should get half bet back
    # Bet 10, get 5 back
    assert mock_player.bankroll == initial_bankroll - 10 + 5


def test_run_full_game_push(mock_dealing_device, mock_player, basic_rules, basic_limits):
    """Integration test where player and dealer push."""
    # Setup cards for initial deal
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)],  # Player (19)
        [Card(Rank.TEN, Suit.DIAMOND), Card(Rank.FIVE, Suit.CLUB)],  # Dealer (15)
    ]
    
    # Player will stand
    mock_player.decision_strategy.decide.return_value = Action.STAND
    
    # Dealer hits to 19
    mock_dealing_device.next_card.return_value = Card(Rank.FOUR, Suit.SPADE)  # Total 19
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    initial_bankroll = mock_player.bankroll
    
    engine.run()
    
    # Player should push (get bet back)
    assert mock_player.bankroll == initial_bankroll - 10 + 10


def test_run_full_game_multiple_players(
    mock_dealing_device, basic_rules, basic_limits
):
    """Integration test with multiple players."""
    from unittest.mock import Mock
    from casino.blackjack.domain import Player
    from casino.blackjack.betting import BettingStrategy
    from casino.blackjack.decision import DecisionStrategy
    
    # Create multiple players
    players = []
    for i in range(3):
        betting_strategy = Mock(spec=BettingStrategy)
        betting_strategy.bet.return_value = 10
        decision_strategy = Mock(spec=DecisionStrategy)
        decision_strategy.decide.return_value = Action.STAND
        player = Player(
            player_id=i,
            name=f"Player {i}",
            bankroll=1000,
            decision_strategy=decision_strategy,
            betting_strategy=betting_strategy,
        )
        players.append(player)
    
    # Setup cards for initial deal
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)],    # Player 0 (19)
        [Card(Rank.TEN, Suit.DIAMOND), Card(Rank.EIGHT, Suit.CLUB)],  # Player 1 (18)
        [Card(Rank.TEN, Suit.HEART), Card(Rank.SEVEN, Suit.SPADE)],   # Player 2 (17)
        [Card(Rank.TEN, Suit.CLUB), Card(Rank.FIVE, Suit.DIAMOND)],   # Dealer (15)
    ]
    
    # Dealer hits to 18
    mock_dealing_device.next_card.return_value = Card(Rank.THREE, Suit.HEART)  # Total 18
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=players,
        rules=basic_rules,
        limits=basic_limits,
    )
    
    initial_bankrolls = [p.bankroll for p in players]
    
    engine.run()
    
    # Player 0 wins (19 vs 18): +20
    assert players[0].bankroll == initial_bankrolls[0] - 10 + 20
    # Player 1 pushes (18 vs 18): +10
    assert players[1].bankroll == initial_bankrolls[1] - 10 + 10
    # Player 2 loses (17 vs 18): +0
    assert players[2].bankroll == initial_bankrolls[2] - 10


def test_run_full_game_dealer_blackjack_no_peak(
    mock_dealing_device, mock_player, no_peak_rules, basic_limits
):
    """Integration test with dealer blackjack and no peak rule."""
    # Setup cards for initial deal (dealer gets only 1 card)
    mock_dealing_device.deal.side_effect = [
        [Card(Rank.TEN, Suit.SPADE), Card(Rank.NINE, Suit.HEART)],  # Player (19)
        [Card(Rank.ACE, Suit.DIAMOND)],  # Dealer (only upcard)
    ]
    
    # Player will stand
    mock_player.decision_strategy.decide.return_value = Action.STAND
    
    # Dealer gets hole card (blackjack)
    mock_dealing_device.next_card.return_value = Card(Rank.KING, Suit.CLUB)
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=no_peak_rules,
        limits=basic_limits,
    )
    
    initial_bankroll = mock_player.bankroll
    
    engine.run()
    
    # Player should lose to dealer blackjack
    assert mock_player.bankroll == initial_bankroll - 10

