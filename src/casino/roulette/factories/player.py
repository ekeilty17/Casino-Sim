from ..config import PlayerConfig
from ..domain import Player
from .betting_strategy import BettingStrategyFactory


class PlayerFactory:
    """Factory for creating Player instances from configuration."""
    
    _id_counter = 0
    
    @classmethod
    def create(cls, config: PlayerConfig) -> Player:
        """
        Create a Player instance from configuration.
        
        Args:
            config: Configuration for the player (includes bankroll)
            
        Returns:
            Configured Player instance
        """
        cls._id_counter += 1
        
        # betting_strategy = BettingStrategyFactory.create_betting_strategy(config)
        
        return Player(
            player_id=cls._id_counter,
            name=config.name,
            bankroll=config.bankroll,
            # betting_strategy=betting_strategy,
        )
    
    @classmethod
    def reset_counter(cls):
        """Reset the player ID counter. Useful for testing."""
        cls._id_counter = 0
