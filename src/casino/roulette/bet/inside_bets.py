from .base import Bet
from ..domain import RouletteNumber

class StraightBet(Bet):

    def __init__(
        self, 
        number: RouletteNumber,
    ) -> None:
        super().__init__(wagered_numbers=[number])

class SplitBet(Bet):

    def __init__(
        self, 
        number1: RouletteNumber, 
        number2: RouletteNumber,
    ) -> None:
        super().__init__(wagered_numbers=[number1, number2])

class ZeroSplitBet(SplitBet):

    def __init__(self) -> None:
        super().__init__(number1=RouletteNumber.ZERO, number2=RouletteNumber.DOUBLE_ZERO)

class StreetBet(Bet):

    def __init__(
        self, 
        number1: RouletteNumber, 
        number2: RouletteNumber, 
        number3: RouletteNumber,
    ) -> None:
        super().__init__(wagered_numbers=[number1, number2, number3])

class CornerBet(Bet):

    def __init__(
        self, 
        number1: RouletteNumber, 
        number2: RouletteNumber, 
        number3: RouletteNumber,
        number4: RouletteNumber,
    ) -> None:
        super().__init__(wagered_numbers=[number1, number2, number3, number4])

class BasketBet(Bet):

    def __init__(
        self, 
        number1: RouletteNumber, 
        number2: RouletteNumber, 
        number3: RouletteNumber,
        number4: RouletteNumber,
        number5: RouletteNumber,
    ) -> None:
        super().__init__(wagered_numbers=[number1, number2, number3, number4, number5])

class LineBet(Bet):

    def __init__(
        self, 
        number1: RouletteNumber, 
        number2: RouletteNumber, 
        number3: RouletteNumber,
        number4: RouletteNumber,
        number5: RouletteNumber,
        number6: RouletteNumber,
    ) -> None:
        super().__init__(wagered_numbers=[number1, number2, number3, number4, number5, number6])