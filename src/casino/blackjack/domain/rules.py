# from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Optional

class DoubleRule(Enum):
    NEVER = "never"
    ANY = "any"
    SPECIFIC_TOTALS = "specific_totals"

class SurrenderRule(Enum):
    NEVER = "never"
    LATE = "late"
    EARLY = "early"

@dataclass(frozen=True)
class Rules:
    """
    Domain value object representing blackjack game rules.
    
    This is an immutable value object that encapsulates all game rules
    with proper enum types. It's constructed by the bootstrapper from
    RulesConfig (the config DTO).
    """
    dealer_hits_soft_17: bool
    blackjack_payout: float
    double_after_split: bool
    resplit_aces: bool
    hit_after_split_aces: bool
    surrender: SurrenderRule
    dealer_peak: bool
    
    # default
    double: DoubleRule = DoubleRule.ANY
    double_allowed_totals: FrozenSet[int] = frozenset()  # only if double=DoubleRule.SPECIFIC_TOTALS
    max_splits: int | None = None