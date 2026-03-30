from dataclasses import dataclass

@dataclass(frozen=True)
class PlayerConfig:
    """
    Configuration DTO for player setup.
    
    This is a pure data transfer object that holds validated configuration
    without resolving to actual strategy instances. The factory layer
    handles the resolution of strategy names to concrete implementations.
    
    This keeps the config layer simple and moves all object construction
    logic to the factory, maintaining consistent separation of concerns
    with Rules and Limits (which are value objects, not config objects).
    """
    name: str
    bankroll: int
    decision_strategy: str
    betting_strategy: str

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerConfig":
        """
        Parse and validate player configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary
            
        Returns:
            Validated PlayerConfig instance
        """
        return cls(
            name=data["name"],
            bankroll=data["bankroll"],
            decision_strategy=data["decision_strategy"],
            betting_strategy=data["betting_strategy"],
        )