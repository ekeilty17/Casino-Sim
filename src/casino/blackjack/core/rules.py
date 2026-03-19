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
class BlackjackRules:
    dealer_hits_soft_17: bool
    blackjack_payout: float
    double: DoubleRule = DoubleRule.ANY
    double_after_split: bool
    resplit_aces: bool
    hit_after_split_aces: bool
    surrender: SurrenderRule
    dealer_peak: bool
    
    # default
    double_allowed_totals: FrozenSet[int] = frozenset()  # only if double=DoubleRule.SPECIFIC_TOTALS
    max_splits: Optional[int] = None


LAS_VEGAS_STRIP_RULES = BlackjackRules(
    dealer_hits_soft_17=False,
    blackjack_payout=1.5,
    double=DoubleRule.ANY,
    double_after_split=True,
    resplit_aces=True,
    hit_after_split_aces=True,
    max_splits=3,
    surrender=SurrenderRule.LATE,
    dealer_peak=False
)

LAS_VEGAS_DOWNTOWN_RULES = BlackjackRules(
    dealer_hits_soft_17=True,
    blackjack_payout=1.5,
    double_after_split=True,
    double=DoubleRule.ANY,
    resplit_aces=True,
    hit_after_split_aces=True,
    max_splits=3,
    surrender=SurrenderRule.NEVER,
    dealer_peak=False
)

EUROPEAN_RULES = BlackjackRules(
    dealer_hits_soft_17=False,
    blackjack_payout=1.5,
    double=DoubleRule.SPECIFIC_TOTALS,
    double_allowed_totals=frozenset([9, 10, 11]),
    double_after_split=False,
    resplit_aces=False,
    hit_after_split_aces=False,
    max_splits=1,
    surrender=SurrenderRule.NEVER,
    dealer_peak=True,
)

if __name__ == "__main__":
    print(LAS_VEGAS_STRIP_RULES)
    print()
    print(LAS_VEGAS_DOWNTOWN_RULES)
    print()
    print(EUROPEAN_RULES)