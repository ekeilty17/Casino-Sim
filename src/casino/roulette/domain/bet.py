from dataclasses import dataclass, field
from typing import Tuple, Optional, Set, Dict
from enum import Enum

from . import RouletteNumber

class BetGroup(Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"
    SPECIAL = "special"

class BetKind(Enum):
    STRAIGHT = "straight"
    SPLIT = "split"
    STREET = "street"
    CORNER = "corner"
    LINE = "line"

    COLUMN = "column"
    DOZEN = "dozen"
    HIGH_LOW = "high_low"
    EVEN_ODD = "even_odd"
    RED_BLACK = "red_black"

    FIXED_SET = "fixed_set"  # all configurable/special bets

@dataclass(frozen=True)
class BetDefinition:
    name: str
    group: BetGroup
    kind: BetKind
    odds: int
    numbers: Optional[Tuple[RouletteNumber, ...]] = None

    def __hash__(self) -> int:
        return hash(self.name)

    def __post_init__(self) -> None:
        if self.group == BetGroup.INSIDE:
            if self.kind not in [BetKind.STRAIGHT, BetKind.SPLIT, BetKind.STREET, BetKind.CORNER, BetKind.LINE]:
                raise Exception("TODO")
        
        if self.group == BetGroup.OUTSIDE:
            if self.kind not in [BetKind.COLUMN, BetKind.DOZEN, BetKind.HIGH_LOW, BetKind.EVEN_ODD, BetKind.RED_BLACK]:
                raise Exception("TODO")
        
        if self.group == BetGroup.SPECIAL:
            if self.kind != BetKind.FIXED_SET:
                raise Exception("TODO")

@dataclass
class BetCatalog:
    catalog: Dict[str, BetDefinition]
    _by_kind_single: Dict[BetKind, BetDefinition] = field(default_factory=dict)
    _by_kind_multi: Dict[BetKind, Set[BetDefinition]] = field(default_factory=dict)
    _by_group: Dict[BetGroup, Set[BetDefinition]] = field(default_factory=dict)

    def __post_init__(self):
        self._by_kind_multi = {kind: set() for kind in BetKind}
        self._by_group = {group: set() for group in BetGroup}
        
        for bet in self.catalog.values():
            if bet.group in {BetGroup.INSIDE, BetGroup.OUTSIDE}:
                if bet.kind in self._by_kind_single:
                    raise ValueError(f"Duplicate bet for kind {bet.kind}")
                self._by_kind_single[bet.kind] = bet
            
            self._by_kind_multi[bet.kind].add(bet)
            self._by_group[bet.group].add(bet)
                
    
    def get(self, name: str) -> BetDefinition:
        return self.catalog[name]

    def get_by_kind(self, kind: BetKind) -> BetDefinition:
        if kind == BetKind.FIXED_SET:
            raise ValueError("BetKind.FIXED_SET does not have a single entry.")
        return self._by_kind_single[kind]

    def get_all_by_kind(self, kind: BetKind) -> Set[BetDefinition]:
        return self._by_kind_multi[kind]

    def get_all_by_group(self, group: BetGroup) -> Set[BetDefinition]:
        return self._by_group[group]

    def get_all(self) -> Set[BetDefinition]:
        return set(self.catalog.values())

@dataclass(frozen=True)
class Bet:
    definition: BetDefinition
    wagered_numbers: Tuple[RouletteNumber, ...]
    stake: int

    def is_win(self, winning_numbers: Set[RouletteNumber]) -> bool:
        return any(number in winning_numbers for number in self.wagered_numbers)

    # def calculate_payout(self) -> int:
    #     stake = self.stake
    #     odds = self.definition.odds
    #     return stake * (odds + 1)


class BetBuilder:
    def _validate_stake(self, stake: int) -> None:
        if stake <= 0:
            raise ValueError("Stake must be positive")

    def _normalize_numbers(
        self, numbers: Tuple[RouletteNumber, ...]
    ) -> Tuple[RouletteNumber, ...]:
        return tuple(sorted(numbers))

class StraightBetBuilder(BetBuilder):
    def build(self, catalog: BetCatalog, layout, numbers, stake):
        self._validate_stake(stake)

        if len(numbers) != 1:
            raise ValueError("Straight requires exactly 1 number")

        number = numbers[0]

        if number not in layout.valid_numbers:
            raise ValueError(f"Invalid number: {number}")

        definition = catalog.get_by_kind(BetKind.STRAIGHT).pop()
        return Bet(definition, (number,), stake)

class BetBuilderRegistry:
    def __init__(self):
        self._builders: Dict[BetKind, BetBuilder] = {}

    def register(self, kind: BetKind, builder: BetBuilder):
        self._builders[kind] = builder

    def get(self, kind: BetKind) -> BetBuilder:
        try:
            return self._builders[kind]
        except KeyError:
            raise ValueError(f"No builder registered for {kind}")