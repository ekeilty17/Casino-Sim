from typing import List

from ..domain import RouletteNumber

class Bet:

    def __init__(self, wagered_numbers: List[RouletteNumber]) -> None:
        self._wagered_numbers = wagered_numbers

    def did_bet_hit(self, winning_number: RouletteNumber) -> bool:
        return winning_number in self._wagered_numbers