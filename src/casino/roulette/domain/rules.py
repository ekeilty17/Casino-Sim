from dataclasses import dataclass

@dataclass(frozen=True)
class Rules:
    min_bet: int
    max_bet: int