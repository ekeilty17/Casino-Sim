"""
Tests for Engine initialization.

Tests the basic initialization of the Engine class and its attributes.
"""

import pytest

from casino.blackjack.engine import Engine


def test_engine_initialization(mock_dealing_device, mock_player, basic_rules, basic_limits):
    """Test engine initializes with correct attributes."""
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=basic_rules,
        limits=basic_limits,
    )
    
    assert engine.dealing_device == mock_dealing_device
    assert engine.players == [mock_player]
    assert engine.rules == basic_rules
    assert engine.limits == basic_limits
    assert engine.dealer_strategy is not None


def test_engine_initialization_multiple_players(
    mock_dealing_device, mock_player, rich_player, basic_rules, basic_limits
):
    """Test engine initializes with multiple players."""
    players = [mock_player, rich_player]
    
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=players,
        rules=basic_rules,
        limits=basic_limits,
    )
    
    assert engine.players == players
    assert len(engine.players) == 2


def test_engine_initialization_with_restrictive_rules(
    mock_dealing_device, mock_player, restrictive_rules, basic_limits
):
    """Test engine initializes with restrictive rules."""
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[mock_player],
        rules=restrictive_rules,
        limits=basic_limits,
    )
    
    assert engine.rules == restrictive_rules
    assert not engine.rules.double_after_split
    assert not engine.rules.resplit_aces


def test_engine_initialization_with_high_stakes(
    mock_dealing_device, rich_player, basic_rules, high_stakes_limits
):
    """Test engine initializes with high stakes limits."""
    engine = Engine(
        dealing_device=mock_dealing_device,
        players=[rich_player],
        rules=basic_rules,
        limits=high_stakes_limits,
    )
    
    assert engine.limits == high_stakes_limits
    assert engine.limits.min_bet == 100
    assert engine.limits.max_bet == 10000

