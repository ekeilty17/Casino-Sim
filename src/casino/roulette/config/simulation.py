from dataclasses import dataclass
from typing import List

from .player import PlayerConfig
from .bets import BetsConfig
from .rules import RulesConfig
from .wheel import WheelConfig
from .limits import LimitsConfig


@dataclass(frozen=True)
class SimulationConfig:
    """
    Top-level configuration DTO for roulette simulations.
    """
    title: str
    players: List[PlayerConfig]
    wheel: WheelConfig
    bets: BetsConfig
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
            players=[PlayerConfig.from_dict(player) for player in data["players"]],
            wheel=WheelConfig.from_dict(data["wheel"]),
            bets=BetsConfig.from_dict(data["bets"]),
            rules=RulesConfig.from_dict(data["rules"]),
            limits=LimitsConfig.from_dict(data["limits"]),
            seed=data.get("seed"),
        )