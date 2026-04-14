from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LimitsConfig:
    """
    Configuration DTO for table betting limits.
    """
    min_bet: int = 1
    max_bet: int | None = None
    max_table_bet: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "LimitsConfig":
        """
        Parse and validate limits configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary
            
        Returns:
            Validated LimitsConfig instance
        """
        return cls(
            min_bet=data.get("min_bet", 1),
            max_bet=data.get("max_bet"),
            max_table_bet=data.get("max_table_bet"),
        )