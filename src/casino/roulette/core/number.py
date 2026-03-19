from enum import Enum

class RoutelletNumber(Enum):
    DOUBLE_ZERO     = ("00", "green")
    ZERO            = ("0", "green")
    ONE             = ()
    TWO             = ()
    THREE             = ()
    FOUR             = ()
    FIVE             = ()
    SIX             = ()
    SEVEN             = ()
    EIGHT             = ()
    NINE             = ()
    TEN             = ()

    def __str__(self):
        return self.value