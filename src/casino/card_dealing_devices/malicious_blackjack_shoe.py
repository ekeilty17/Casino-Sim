import random
from typing import Iterable, Any, List

from casino.core.card import Card, Pip
from casino.card_dealing_devices.shoe import Shoe


class MaliciousBlackJackShoe(Shoe):

    def shuffle(self) -> None:
        """Implement malicious shuffle algorithm to make BlackJack unbeatable"""
        # TODO: Test
        self.num_groups = 3
        
        low_card_pips = [Pip.TWO, Pip.THREE, Pip.FOUR, Pip.FIVE, Pip.SIX]
        middle_card_pips = [Pip.SEVEN, Pip.EIGHT, Pip.NINE]
        high_card_pips = [Pip.TEN, Pip.JACK, Pip.QUEEN, Pip.KING, Pip.ACE]
        pip_groups = [
            low_card_pips, middle_card_pips, high_card_pips
        ]

        cards: List[Card] = self._deck.get_cards()
        card_groups: List[List[Card]] = [
            [card for card in cards if card.pip in pip_group] 
            for pip_group in pip_groups
        ]
        for group in card_groups:
            self._rng.shuffle(group)
        
        partitioned_card_groups: List[List[List[Card]]] = [
            MaliciousBlackJackShoe._partition(group, self.num_groups) 
            for group in card_groups
        ]

        merged_partitions: List[List[Card]] = [
            MaliciousBlackJackShoe._merge(groups)
            for groups in zip(partitioned_card_groups)
        ]
        for partition in merged_partitions:
            self._rng.shuffle(partition)

        malicious_cards: List[Card] = MaliciousBlackJackShoe._merge(merged_partitions)
        self._deck.stack(malicious_cards)

    @staticmethod
    def _partition(lst: Iterable[Any], num_groups: int) -> List[Any]:
        lst = list(lst)
        n = len(lst)
        
        if num_groups <= 0:
            raise ValueError("num_groups must be greater than 0")
        
        # Determine base size and remainder
        k, m = divmod(n, num_groups)
        
        partitions = []
        start = 0
        
        for i in range(num_groups):
            # First m groups get an extra element
            end = start + k + (1 if i < m else 0)
            partitions.append(lst[start:end])
            start = end
        
        return partitions
    
    @staticmethod
    def _merge(lsts: List[Iterable[Any]]) -> List[Any]:
        return [item for lst in lsts for item in lst]