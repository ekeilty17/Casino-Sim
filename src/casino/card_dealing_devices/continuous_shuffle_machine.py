from core.card import Card
from card_dealing_devices.card_dealing_device import CardDealingDevice


class ContinuousShuffleMachine(CardDealingDevice):
    """
    A simplified Continuous Shuffle Machine (CSM) model.

    This model does NOT simulate a physical CSM's internal mechanics exactly.
    Instead, it approximates its effect from a gameplay/simulation perspective:
    each round effectively begins with a freshly shuffled deck.
    """

    def shuffle(self) -> None:
        """
        Reset and shuffle the entire deck.
        """
        self._deck.reset()
        self._deck.shuffle()

    def discard(self, *cards: Card) -> None:
        """
        Discarded cards are ignored in this model.

        Unlike a shoe, a continuous shuffle machine does not maintain a
        discard pile across rounds. Since the entire deck is reset and
        shuffled at the end of each round, discards do not need to be tracked.

        This method is intentionally a no-op to satisfy the abstract interface.
        """
        return

    def needs_shuffle(self) -> bool:
        """
        Indicates whether a shuffle should occur.

        In this simplified CSM model, a shuffle is always expected at the
        end of each round. This simulate "reinjecting" the discarded cards back into the deck.
        Mathematically, this is equivalent to a full reshuffle.

        Returns:
            bool: Always True.
        """
        return True