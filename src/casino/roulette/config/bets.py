from dataclasses import dataclass
from typing import List, Optional, Dict


# TODO: Maybe add this feature in the future, but I don't want to over-complicate for now
@dataclass(frozen=True)
class BetRequirements:
    """
    Requirements for a bet to be available.
    """
    min_zeros: Optional[int] = None
    max_zeros: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "BetRequirements":
        """
        Parse bet requirements from raw dict.
        
        Args:
            data: Raw requirements dictionary
            
        Returns:
            Validated BetRequirements instance
        """
        return cls(
            min_zeros=data.get("min_zeros"),
            max_zeros=data.get("max_zeros"),
        )


@dataclass(frozen=True)
class BetDefinitionConfig:
    """
    Configuration DTO for a single bet.
    """
    name: str
    kind: str
    group: str
    odds: int
    numbers: Optional[List[str]] = None
    # requires: Optional[BetRequirements] = None

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "BetDefinitionConfig":
        """
        Parse and validate bet configuration from raw dict.
        
        Args:
            name: The bet name/key from the config
            data: Raw configuration dictionary for this bet
            
        Returns:
            Validated BetDefinitionConfig instance
        """
        requires = None
        if "requires" in data:
            requires = BetRequirements.from_dict(data["requires"])
        
        return cls(
            name=name,
            kind=data["kind"],
            group=data["group"],
            odds=data["odds"],
            numbers=data.get("numbers"),
            # requires=requires,
        )


@dataclass(frozen=True)
class BetsConfig:
    """
    Configuration DTO for all roulette bets.
    """
    definitions: Dict[str, BetDefinitionConfig]

    @classmethod
    def from_dict(cls, data: dict) -> "BetsConfig":
        """
        Parse and validate bets configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary with bet definitions
            
        Returns:
            Validated BetsConfig instance
        """
        definitions = {
            bet_name: BetDefinitionConfig.from_dict(bet_name, bet_data)
            for bet_name, bet_data in data.items()
        }
        
        return cls(definitions=definitions)
