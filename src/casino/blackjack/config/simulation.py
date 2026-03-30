from dataclasses import dataclass
from typing import Optional, List

from casino.blackjack.config.dealing import DealingConfig
from casino.blackjack.config.player import PlayerConfig
from casino.blackjack.config.rules import RulesConfig
from casino.blackjack.config.limits import LimitsConfig


@dataclass(frozen=True)
class SimulationConfig:
    """
    Top-level configuration DTO for blackjack simulations.
    
    This is a pure data transfer object that holds all configuration DTOs.
    It maintains consistent separation: all fields are config objects,
    not domain objects. The bootstrapper layer handles conversion to
    domain objects (Rules, Limits, Player, etc.).
    """
    title: str
    dealing: DealingConfig
    players: List[PlayerConfig]
    rules: RulesConfig
    limits: LimitsConfig
    seed: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "SimulationConfig":
        """
        Parse and validate simulation configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary (e.g., from YAML)
            
        Returns:
            Validated SimulationConfig instance with all sub-configs parsed
        """
        return cls(
            title=data["title"],
            dealing=DealingConfig.from_dict(data["dealing"]),
            players=[PlayerConfig.from_dict(player) for player in data["players"]],
            rules=RulesConfig.from_dict(data["rules"]),
            limits=LimitsConfig.from_dict(data["limits"]),
            seed=data.get("seed"),
        )