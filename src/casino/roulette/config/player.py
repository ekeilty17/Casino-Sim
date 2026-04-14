from dataclasses import dataclass

@dataclass(frozen=True)
class PlayerConfig:
    """
    Configuration DTO for player setup.
    """
    name: str
    bankroll: int
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
            betting_strategy=data["betting_strategy"],
        )