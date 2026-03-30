from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Limits:
    """
    Domain value object representing table betting limits.
    
    This is an immutable value object that encapsulates betting limits
    with validation logic. It's constructed by the bootstrapper from
    LimitsConfig (the config DTO).
    """
    min_bet: Optional[int] = 1
    max_bet: Optional[int] = None
    max_table_bet: Optional[int] = None

    def __post_init__(self):
        """Validate betting limits constraints."""
        if self.min_bet is not None and self.min_bet < 1:
            raise ValueError("min_bet must be >= 1")
        
        if self.min_bet is not None and self.max_bet is not None and self.min_bet > self.max_bet:
            raise ValueError("min_bet must be <= max_bet")
        
        if self.max_bet is not None and self.max_table_bet is not None and self.max_bet > self.max_table_bet:
            raise ValueError("max_bet must be <= max_table_bet")