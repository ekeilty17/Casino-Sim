from enum import Enum
from typing import Dict

class RouletteColor(Enum):
    RED = "red"
    BLACK = "black"
    GREEN = "green"

class RouletteNumber(Enum):
    DOUBLE_ZERO     = ("00", 0,  RouletteColor.GREEN)
    ZERO            = ("0",  0,  RouletteColor.GREEN)
    ONE             = ("1",  1,  RouletteColor.RED)
    TWO             = ("2",  2,  RouletteColor.BLACK)
    THREE           = ("3",  3,  RouletteColor.RED)
    FOUR            = ("4",  4,  RouletteColor.BLACK)
    FIVE            = ("5",  5,  RouletteColor.RED)
    SIX             = ("6",  6,  RouletteColor.BLACK)
    SEVEN           = ("7",  7,  RouletteColor.RED)
    EIGHT           = ("8",  8,  RouletteColor.BLACK)
    NINE            = ("9",  9,  RouletteColor.RED)
    TEN             = ("10", 10, RouletteColor.BLACK)
    ELEVEN          = ("11", 11, RouletteColor.BLACK)
    TWELVE          = ("12", 12, RouletteColor.RED)
    THIRTEEN        = ("13", 13, RouletteColor.BLACK)
    FOURTEEN        = ("14", 14, RouletteColor.BLACK)
    FIFTEEN         = ("15", 15, RouletteColor.RED)
    SIXTEEN         = ("16", 16, RouletteColor.BLACK)
    SEVENTEEN       = ("17", 17, RouletteColor.RED)
    EIGHTEEN        = ("18", 18, RouletteColor.RED)
    NINETEEN        = ("19", 19, RouletteColor.RED)
    TWENTY          = ("20", 20, RouletteColor.BLACK)
    TWENTY_ONE      = ("21", 21, RouletteColor.RED)
    TWENTY_TWO      = ("22", 22, RouletteColor.BLACK)
    TWENTY_THREE    = ("23", 23, RouletteColor.RED)
    TWENTY_FOUR     = ("24", 24, RouletteColor.BLACK)
    TWENTY_FIVE     = ("25", 25, RouletteColor.RED)
    TWENTY_SIX      = ("26", 26, RouletteColor.BLACK)
    TWENTY_SEVEN    = ("27", 27, RouletteColor.RED)
    TWENTY_EIGHT    = ("28", 28, RouletteColor.BLACK)
    TWENTY_NINE     = ("29", 29, RouletteColor.BLACK)
    THIRTY          = ("30", 30, RouletteColor.RED)
    THIRTY_ONE      = ("31", 31, RouletteColor.BLACK)
    THIRTY_TWO      = ("32", 32, RouletteColor.RED)
    THIRTY_THREE    = ("33", 33, RouletteColor.BLACK)
    THIRTY_FOUR     = ("34", 34, RouletteColor.RED)
    THIRTY_FIVE     = ("35", 35, RouletteColor.BLACK)
    THIRTY_SIX      = ("36", 36, RouletteColor.RED)

    def __init__(self, label, numeric_value, color):
        self.label = label
        self.numeric_value = numeric_value
        self.color = color

    def is_red(self) -> bool:
        """Determines if the roulette number is red."""
        return self.color == RouletteColor.RED

    def is_black(self) -> bool:
        """Determines if the roulette number is black."""
        return self.color == RouletteColor.BLACK

    def is_green(self) -> bool:
        """Determines if the roulette number is green (0 or 00)."""
        return self.color == RouletteColor.GREEN

    def is_between(self, lower: int, upper: int) -> bool:
        """Determines if the roulette number is between lower and upper (inclusive)"""
        return lower <= self.numeric_value <= upper

    def is_even(self) -> bool:
        """Determines if the number is even. Note that 0 and 00 don't count as even."""
        return not self.is_zero_or_double_zero() and self.numeric_value % 2 == 0

    def is_odd(self) -> bool:
        """Determines if the number is odd. Note that 0 and 00 don't count as odd."""
        return not self.is_zero_or_double_zero() and self.numeric_value % 2 == 1

    def is_zero_or_double_zero(self) -> bool:
        """Determines if the number is either ZERO or DOUBLE_ZERO."""
        return self in {RouletteNumber.ZERO, RouletteNumber.DOUBLE_ZERO}

    @classmethod
    def from_numeric_value(cls, numeric_value: int) -> "RouletteNumber":
        """
        Class method to retrieve a RouletteNumber instance based on its numeric value.

        Args:
            numeric_value (int): The numeric value to search for.

        Returns:
            RouletteNumber: The corresponding RouletteNumber enum member.

        Raises:
            ValueError: If no matching RouletteNumber is found for the given numeric value.
        """
        if numeric_value == 0:
            return RouletteNumber.ZERO

        lookup: Dict[int, RouletteNumber] = {num.numeric_value: num for num in cls}
        
        try:
            return lookup[numeric_value]
        except KeyError:
            raise ValueError(f"Invalid numeric value: {numeric_value}")

    @classmethod
    def from_label(cls, label: str) -> "RouletteNumber":
        """
        Class method to retrieve a RouletteNumber instance based on its label.

        Args:
            label (str): The label to search for (e.g., "00", "0", "1", etc.).

        Returns:
            RouletteNumber: The corresponding RouletteNumber enum member.

        Raises:
            ValueError: If no matching RouletteNumber is found for the given label.
        """
        lookup: Dict[str, RouletteNumber] = {num.label: num for num in cls}
        
        try:
            return lookup[label]
        except KeyError:
            raise ValueError(f"Invalid label: {label}")