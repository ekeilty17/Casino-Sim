from typing import List

from .base import Bet
from ..domain import RouletteNumber

class ColumnBet(Bet):

    def __init__(self, column: List[RouletteNumber]) -> None:
        super().__init__(wagered_numbers=column)

class DozenBet(Bet):

    def __init__(self, dozen: List[RouletteNumber]) -> None:
        super().__init__(wagered_numbers=dozen)

class RedBet(Bet):

    def __init__(self) -> None:
        wagered_numbers = [number for number in RouletteNumber if number.is_red()]
        super().__init__(wagered_numbers=wagered_numbers)

class BlackBet(Bet):

    def __init__(self) -> None:
        wagered_numbers = [number for number in RouletteNumber if number.is_black()]
        super().__init__(wagered_numbers=wagered_numbers)

class EvenBet(Bet):
    def __init__(self) -> None:
        wagered_numbers = [number for number in RouletteNumber if number.is_even()]
        super().__init__(wagered_numbers=wagered_numbers)

class OddBet(Bet):
    def __init__(self) -> None:
        wagered_numbers = [number for number in RouletteNumber if number.is_odd()]
        super().__init__(wagered_numbers=wagered_numbers)