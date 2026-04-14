from typing import List, Set, Container, Dict

from casino.roulette.domain.bet import Bet, BetDefinition, BetKind, BetGroup, BetCatalog

from . import RouletteNumber
from .bet import *

class RouletteTable:

    GRID_WIDTH = 3
    GRID_HEIGHT = 12

    def __init__(self) -> None:
        self._grid: List[List[RouletteNumber]] = self._construct_grid()

    def _construct_grid(self) -> List[List[RouletteNumber]]:
        return [
            [
                RouletteNumber.from_label( str(self.GRID_WIDTH*k + n + 1) ) for n in range(self.GRID_WIDTH)
            ] for k in range(self.GRID_HEIGHT)
        ]

    def _get_row(self, index: int) -> List[RouletteNumber]:
        return self._grid[index]
    
    def _get_col(self, index: int) -> List[RouletteNumber]:
        return [row[index] for row in self._grid]

    def validate_bet(self, bet: Bet) -> bool:
        pass

    def _get_allowed_bets(self) -> Set[Bet]:
        bets = {
            BetKind.STRAIGHT: self._get_straight_bets(),
            BetKind.SPLIT: self._get_split_bets(),
            BetKind.STREET: self._get_street_bets(),
            BetKind.CORNER: self._get_corner_bets(),
            BetKind.LINE: self._get_line_bets(),
            
            BetKind.COLUMN: self._get_column_bets(),
            BetKind.DOZEN: self._get_dozen_bets(),
            BetKind.HIGH_LOW: self._get_high_low_bets(),
            BetKind.EVEN_ODD: self._get_odd_even_bets(),
            BetKind.RED_BLACK: self._get_red_black_bets(),
        }
        return set().union(*bets.values())

    def _get_straight_bets(self) -> Set[Bet]:
        straight_bets: Set[StraightBet] = set([])
        for row in self._grid:
            for number in row:
                straight_bets.add( StraightBet(number) )
        return straight_bets

    def _get_split_bets(self) -> Set[SplitBet]:
        split_bets: Set[SplitBet] = set([])

        for i in range(self.GRID_HEIGHT):
            row = self._get_row(i)
            for number1, number2 in zip(row[:-1], row[1:]):
                split_bets.add( SplitBet(number1, number2) )

        for j in range(self.GRID_WIDTH):
            col = self._get_col(j)
            for number1, number2 in zip(col[:-1], col[1:]):
                split_bets.add( SplitBet(number1, number2) )

        return split_bets

    def _get_street_bets(self) -> Set[StreetBet]:
        street_bets: Set[StreetBet] = set([])

        for i in range(self.GRID_HEIGHT):
            number1, number2, number3 = self._get_row(i)
            street_bets.add( StreetBet(number1, number2, number3) )

        return street_bets

    def _get_corner_bets(self) -> Set[CornerBet]:
        corner_bets: Set[CornerBet] = set([])

        for i in range(self.GRID_WIDTH-1):
            for j in range(self.GRID_HEIGHT-1):
                number1, number2 = self._grid[i][j:j+2]
                number3, number4 = self._grid[i+1][j:j+2]
                corner_bets.add( CornerBet(number1, number2, number3, number4) )

        return corner_bets

    def _get_line_bets(self) -> Set[LineBet]:
        line_bets: Set[LineBet] = set([])

        for i in range(self.GRID_HEIGHT-1):
            number1, number2, number3 = self._get_row(i)
            number4, number5, number6 = self._get_row(i+1)
            line_bets.add( LineBet(number1, number2, number3, number4, number5, number6) )

        return line_bets

    def _get_column_bets(self) -> Set[FirstColumnBet | SecondColumnBet | ThirdColumnBet]:
        return {FirstColumnBet(), SecondColumnBet(), ThirdColumnBet()}

    def _get_dozen_bets(self) -> Set[FirstDozenBet | SecondDozenBet | ThirdDozenBet]:
        return {FirstDozenBet(), SecondDozenBet(), ThirdDozenBet()}
    
    def _get_high_low_bets(self) -> Set[LowBet | HighBet]:
        return {LowBet(), HighBet()}

    def _get_red_black_bets(self) -> Set[RedBet | BlackBet]:
        return {RedBet(), BlackBet()}
    
    def _get_odd_even_bets(self) -> Set[OddBet | EvenBet]:
        return {OddBet(), EvenBet()}