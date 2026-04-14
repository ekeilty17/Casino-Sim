from casino.blackjack.decision import DecisionStrategy, RandomDecisionStrategy, AlwaysStandDecisionStrategy
from ..config import PlayerConfig

class DecisionStrategyFactory:
    """Factory for creating decision strategy instances from configuration."""
    
    # Map strategy names (case-insensitive) to strategy classes
    _STRATEGY_MAP = {
        "always stand": AlwaysStandDecisionStrategy,
        "random": RandomDecisionStrategy,
        # TODO: Add more strategies as they're implemented
        # "no bust": NoBustDecisionStrategy,
        # "basic strategy": BasicStrategyDecisionStrategy,
        # "high low": HighLowDecisionStrategy,
    }

    @classmethod
    def create_decision_strategy(cls, player_config: PlayerConfig) -> DecisionStrategy:
        """
        Create a decision strategy instance from player configuration.
        
        Args:
            player_config: Player configuration containing strategy name
            
        Returns:
            Instantiated decision strategy
            
        Raises:
            ValueError: If strategy name is not recognized
        """
        strategy_name = player_config.decision_strategy.lower().strip()
        
        if strategy_name not in cls._STRATEGY_MAP:
            valid_strategies = ", ".join(cls._STRATEGY_MAP.keys())
            raise ValueError(
                f"Unknown decision strategy: '{player_config.decision_strategy}'. "
                f"Valid options: {valid_strategies}"
            )
        
        strategy_class = cls._STRATEGY_MAP[strategy_name]
        return strategy_class()