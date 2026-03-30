from enum import Enum

class Action(Enum):
    HIT         = "hit"
    STAND       = "stand"
    SURRENDER   = "surrender"
    DOUBLE      = "double"
    SPLIT       = "split"

    def __str__(self):
        return self.value