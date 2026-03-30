from casino.domain import Card, Rank

class Cards:

    _VALUES = {
        Rank.ACE: 1,
        Rank.TWO: 2,
        Rank.THREE: 3,
        Rank.FOUR: 4,
        Rank.FIVE: 5,
        Rank.SIX: 6,
        Rank.SEVEN: 7,
        Rank.EIGHT: 8,
        Rank.NINE: 9,
        Rank.TEN: 10,
        Rank.JACK: 10,
        Rank.QUEEN: 10,
        Rank.KING: 10,
    }
    _ACE_HIGH_VALUE = 10

    def __init__(self, *cards: Card) -> None:
        if not all(isinstance(card, Card) for card in cards):
            raise TypeError("All items must be Card instances")
        self.cards = list(cards)

    def __str__(self) -> str:
        return ", ".join([str(card) for card in self.cards])
    
    # TODO
    # def __repr__(self) -> str:
    #     return ""

    def __len__(self) -> int:
        return len(self.cards)
    
    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise TypeError("card must be a Card instance")
        self.cards.append(card)

    def _contains_ace(self) -> bool:
        return any(card.rank == Rank.ACE for card in self.cards)

    def _get_lower_bound_total(self) -> int:
        return sum([Cards._VALUES[card.rank] for card in self.cards])

    def is_soft_hand(self) -> bool:
        return self._contains_ace() and self._get_lower_bound_total() <= 11

    def get_total(self) -> int:
        total = self._get_lower_bound_total()
        return total + Cards._ACE_HIGH_VALUE if self.is_soft_hand() else total
    
    def is_blackjack(self) -> bool:
        return self.get_total() == 21 and len(self.cards) == 2

    def is_busted(self) -> bool:
        return self.get_total() > 21
        