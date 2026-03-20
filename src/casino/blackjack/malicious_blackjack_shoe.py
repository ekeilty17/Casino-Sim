import random
from typing import Iterable, Any, List

from casino.core.card import Card
from casino.core.rank import Rank
from casino.dealing.shoe import Shoe


class MaliciousBlackJackShoe(Shoe):

    def shuffle(self) -> None:
        """Implement malicious shuffle algorithm to make BlackJack unbeatable"""
        # TODO: Test
        self.num_groups = 3
        
        low_card_Ranks = [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX]
        middle_card_Ranks = [Rank.SEVEN, Rank.EIGHT, Rank.NINE]
        high_card_Ranks = [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]
        Rank_groups = [
            low_card_Ranks, middle_card_Ranks, high_card_Ranks
        ]

        cards: List[Card] = self._deck.get_cards()
        card_groups: List[List[Card]] = [
            [card for card in cards if card.Rank in Rank_group] 
            for Rank_group in Rank_groups
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