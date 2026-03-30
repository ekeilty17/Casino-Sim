from casino.domain import Card, Rank


class BlackjackEvaluator:
    """
    Stateless utility for blackjack card calculations.
    
    Provides primitive operations on cards. Does not make game decisions
    or determine what actions are possible - that's the Hand's job.
    """
    
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
    _SOFT_ACE_BONUS = 10
    
    @classmethod
    def get_card_value(cls, rank: Rank) -> int:
        """Get the base value of a card rank in blackjack"""
        return cls._VALUES[rank]
    
    @classmethod
    def get_card_values(cls, cards: list[Card]) -> list[int]:
        """
        Get the base blackjack value of each card.
        
        Args:
            cards: List of cards
            
        Returns:
            List of integer values corresponding to each card
        """
        return [cls._VALUES[card.rank] for card in cards]
    
    @classmethod
    def get_total(cls, cards: list[Card]) -> int:
        """Calculate total value of cards, accounting for soft aces"""
        total = sum(cls._VALUES[card.rank] for card in cards)
        if cls._is_soft(cards, total):
            total += cls._SOFT_ACE_BONUS
        return total
    
    @classmethod
    def _is_soft(cls, cards: list[Card], total: int) -> bool:
        """Check if hand is soft (has usable ace counted as 11)"""
        has_ace = any(card.rank == Rank.ACE for card in cards)
        return has_ace and total <= 11
    
    @classmethod
    def is_soft(cls, cards: list[Card]) -> bool:
        """Check if hand is soft (has usable ace counted as 11)"""
        total = sum(cls._VALUES[card.rank] for card in cards)
        return cls._is_soft(cards, total)
    
    @classmethod
    def is_blackjack(cls, cards: list[Card]) -> bool:
        """
        Check if cards form a natural blackjack (21 with exactly 2 cards).
        
        This is a pure card evaluation and does not consider game context
        such as whether the hand resulted from a split.
        
        Returns:
            True if cards total 21 with exactly 2 cards, False otherwise
        """
        return cls.get_total(cards) == 21 and len(cards) == 2
    
    @classmethod
    def is_busted(cls, cards: list[Card]) -> bool:
        """Check if hand is busted (over 21)"""
        return cls.get_total(cards) > 21
