from casino.blackjack.config.player import PlayerConfig
from casino.blackjack.domain.player import Player
from casino.blackjack.factories.betting_strategy import BettingStrategyFactory
from casino.blackjack.factories.decision_strategy import DecisionStrategyFactory


class PlayerFactory:
    """Factory for creating Player instances from configuration."""
    
    _player_id_counter = 0
    
    @classmethod
    def create_player(cls, player_config: PlayerConfig) -> Player:
        """
        Create a Player instance from configuration.
        
        Args:
            player_config: Configuration for the player (includes bankroll)
            
        Returns:
            Configured Player instance
        """
        cls._player_id_counter += 1
        
        decision_strategy = DecisionStrategyFactory.create_decision_strategy(player_config)
        betting_strategy = BettingStrategyFactory.create_betting_strategy(player_config)
        
        return Player(
            player_id=cls._player_id_counter,
            name=player_config.name,
            bankroll=player_config.bankroll,
            decision_strategy=decision_strategy,
            betting_strategy=betting_strategy,
        )
    
    @classmethod
    def reset_counter(cls):
        """Reset the player ID counter. Useful for testing."""
        cls._player_id_counter = 0
