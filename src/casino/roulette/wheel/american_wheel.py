from typing import List

from .base import RouletteWheel
from ..domain.number import RouletteNumber

class AmericanRouletteWheel(RouletteWheel):

    def construct_wheel(self) -> List[RouletteNumber]:
        wheel_label_order: List[str] = [
            "0",
            "28",
            "9",
            "26",
            "30",
            "11",
            "7",
            "20",
            "32",
            "17",
            "5",
            "22",
            "34",
            "15",
            "3",
            "24",
            "36",
            "13",
            "1",
            "00",
            "27",
            "10",
            "25",
            "29",
            "12",
            "8",
            "19",
            "31",
            "18",
            "6",
            "21",
            "33",
            "16",
            "4",
            "23",
            "35",
            "14",
            "2"
        ]
        return [RouletteNumber.from_label(label) for label in wheel_label_order]