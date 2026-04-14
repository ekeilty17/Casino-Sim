from dataclasses import dataclass


@dataclass(frozen=True)
class DealingConfig:
    """
    Configuration DTO for dealing device setup.
    """
    device_type: str
    number_of_decks: int
    penetration: float = 0.8

    @classmethod
    def from_dict(cls, data: dict) -> "DealingConfig":
        """
        Parse and validate dealing configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary
            
        Returns:
            Validated DealingConfig instance
        """
        return cls(
            device_type=data["device"],
            number_of_decks=data["number_of_decks"],
            penetration=data.get("penetration", 0.8),
        )