from typing import List

from .base import RouletteWheel
from ..domain.number import RouletteNumber

class EuropeanRouletteWheel(RouletteWheel):

    def construct_wheel(self) -> List[RouletteNumber]:
        wheel_label_order: List[str] = [
            "0", 
            "32", 
            "15", 
            "19", 
            "4", 
            "21", 
            "2", 
            "25", 
            "17", 
            "34", 
            "6", 
            "27", 
            "13", 
            "36", 
            "11", 
            "30", 
            "8", 
            "23", 
            "10", 
            "5", 
            "24", 
            "16", 
            "33", 
            "1", 
            "20", 
            "14", 
            "31", 
            "9", 
            "22", 
            "18", 
            "29", 
            "7", 
            "28", 
            "12", 
            "35", 
            "3", 
            "26"
        ]
        return [RouletteNumber.from_label(label) for label in wheel_label_order]