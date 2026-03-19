from enum import Enum

class BlackJackAction(Enum):
    HIT         = "hit"
    STAND       = "stand"
    DOUBLE      = "double"
    SPLIT       = "split"
    SURRENDER   = "surrender"

    def __str__(self):
        return self.value