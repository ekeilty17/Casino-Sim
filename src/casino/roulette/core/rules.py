from dataclasses import dataclass

@dataclass(frozen=True)
class RouletteRules:
    min_bet: int
    max_bet: int