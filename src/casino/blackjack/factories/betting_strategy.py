from ..config import PlayerConfig
from ..betting import BettingStrategy, RandomBettingStrategy, FlatBettingStrategy


class BettingStrategyFactory:
    """Factory for creating betting strategy instances from configuration."""
    
    # Map strategy names (case-insensitive) to strategy classes
    _STRATEGY_MAP = {
        "random": RandomBettingStrategy,
        "flat": FlatBettingStrategy,
    }

    @classmethod
    def create_betting_strategy(cls, player_config: PlayerConfig) -> BettingStrategy:
        """
        Create a betting strategy instance from player configuration.
        
        Args:
            player_config: Player configuration containing strategy name
            
        Returns:
            Instantiated betting strategy
            
        Raises:
            ValueError: If strategy name is not recognized
        """
        strategy_name = player_config.betting_strategy.lower().strip()
        
        if strategy_name not in cls._STRATEGY_MAP:
            valid_strategies = ", ".join(cls._STRATEGY_MAP.keys())
            raise ValueError(
                f"Unknown betting strategy: '{player_config.betting_strategy}'. "
                f"Valid options: {valid_strategies}"
            )
        
        strategy_class = cls._STRATEGY_MAP[strategy_name]
        return strategy_class()