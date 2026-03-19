from core.hand import Hand
from core.card import Pip

class BlackJackHand(Hand):

    _card_values = {
        Pip.ACE: 1,
        Pip.TWO: 2,
        Pip.THREE: 3,
        Pip.FOUR: 4,
        Pip.FIVE: 5,
        Pip.SIX: 6,
        Pip.SEVEN: 7,
        Pip.EIGHT: 8,
        Pip.NINE: 9,
        Pip.TEN: 10,
        Pip.JACK: 10,
        Pip.QUEEN: 10,
        Pip.KING: 10,
    }

    def _contains_ace(self) -> bool:
        pips = [card.pip for card in self.cards]
        return Pip.ACE in pips

    def _get_lower_bound_total(self) -> int:
        return sum([BlackJackHand._card_values[card.pip] for card in self.cards])

    def is_soft_hand(self) -> bool:
        return self._contains_ace() and self._get_lower_bound_total() <= 11

    def get_total(self) -> int:
        total = self._get_lower_bound_total()
        return total + 10 if self.is_soft_hand() else total
    
    def is_blackjack(self) -> bool:
        return self.get_total() == 21 and len(self.cards) == 2

    def is_busted(self) -> bool:
        return self.get_total() > 21
    
    def is_splittable(self) -> bool:
        if len(self.cards) != 2:
            return False
        card1, card2 = self.cards
        return BlackJackHand._card_values[card1.pip] == BlackJackHand._card_values[card2.pip]
        