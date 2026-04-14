from dataclasses import dataclass, field
from typing import Optional, List


@dataclass(frozen=True)
class RulesConfig:
    """
    Configuration DTO for blackjack game rules.
    """
    dealer_hits_soft_17: bool
    blackjack_payout: float
    double_after_split: bool
    resplit_aces: bool
    hit_after_split_aces: bool
    surrender: str
    dealer_peak: bool
    double: str = "any"
    double_allowed_totals: List[int] = field(default_factory=list)
    max_splits: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "RulesConfig":
        """
        Parse and validate rules configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary
            
        Returns:
            Validated RulesConfig instance
        """
        return cls(
            dealer_hits_soft_17=data["dealer_hits_soft_17"],
            blackjack_payout=data["blackjack_payout"],
            double_after_split=data["double_after_split"],
            resplit_aces=data["resplit_aces"],
            hit_after_split_aces=data["hit_after_split_aces"],
            surrender=data["surrender"],
            dealer_peak=data["dealer_peak"],
            double=data.get("double", "any"),
            double_allowed_totals=data.get("double_allowed_totals", []),
            max_splits=data.get("max_splits"),
        )
