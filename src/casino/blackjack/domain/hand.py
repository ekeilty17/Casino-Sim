from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

from casino.domain import Card, Rank
from .evaluator import BlackjackEvaluator


class PlayerHandResult(Enum):
    WIN = "win"
    LOSE = "lose"
    PUSH = "push"

    def __str__(self):
        return self.value


@dataclass
class PlayerHand:
    """
    Represents a player's hand with betting and action state.
    
    Tracks the hand's cards, bet amount, and various state flags including
    whether the hand resulted from a split and what rank was split.
    """
    bet: int
    cards: list[Card] = field(default_factory=list)
    is_doubled: bool = False
    is_split: bool = False
    split_from_rank: Optional[Rank] = None  # Rank of cards that were split to create this hand
    is_active: bool = True
    result: Optional[PlayerHandResult] = None

    def add_card(self, card: Card) -> None:
        """Add a card to the hand"""
        self.cards.append(card)

    # Delegate evaluation to BlackjackEvaluator
    def get_total(self) -> int:
        """Get the total value of the hand"""
        return BlackjackEvaluator.get_total(self.cards)

    def is_soft(self) -> bool:
        """Check if hand is soft (has usable ace counted as 11)"""
        return BlackjackEvaluator.is_soft(self.cards)

    def is_blackjack(self) -> bool:
        """
        Check if hand qualifies as a natural blackjack for payout purposes.
        
        A hand is a blackjack if:
        - Cards total 21 with exactly 2 cards (natural)
        - Hand was not created from a split (split aces don't count as blackjack)
        
        Returns:
            True if hand is a paying blackjack, False otherwise
        """
        return not self.is_split and BlackjackEvaluator.is_blackjack(self.cards)

    def is_busted(self) -> bool:
        """Check if hand is busted"""
        return BlackjackEvaluator.is_busted(self.cards)

    # Player-specific actions
    def can_double(self) -> bool:
        """Check if hand can be doubled"""
        return len(self.cards) == 2

    def can_surrender(self) -> bool:
        """Check if hand can be surrendered"""
        return len(self.cards) == 2

    def can_split(self) -> bool:
        """
        Check if hand can be split.
        
        A hand can be split if it has exactly two cards with equal blackjack values.
        Cards with different ranks can have the same value (e.g., 10-J, K-Q).
        
        Returns:
            True if hand has two cards with equal values, False otherwise
        """
        if len(self.cards) != 2:
            return False
        values = BlackjackEvaluator.get_card_values(self.cards)
        return values[0] == values[1]
    
    def split(self) -> tuple['PlayerHand', 'PlayerHand']:
        """
        Split the hand into two separate hands.
        
        Creates two new hands, each with one card from the original pair.
        Both hands are marked as split and track the rank that was split.
        This information is used by the engine to enforce rules like
        "no resplit aces" or "no hit after split aces".
        
        Returns:
            Tuple of two new PlayerHand objects
            
        Raises:
            ValueError: If hand cannot be split (not a pair)
        """
        if not self.can_split():
            raise ValueError("Hand cannot be split")

        card1, card2 = self.cards
        split_rank = card1.rank
        
        hand1 = PlayerHand(
            bet=self.bet,
            cards=[card1],
            is_split=True,
            split_from_rank=split_rank
        )
        hand2 = PlayerHand(
            bet=self.bet,
            cards=[card2],
            is_split=True,
            split_from_rank=split_rank
        )
        return hand1, hand2


@dataclass
class DealerHand:
    """Represents the dealer's hand with hole card mechanics"""
    cards: list[Card] = field(default_factory=list)
    hole_card_revealed: bool = False

    def add_card(self, card: Card) -> None:
        """Add a card to the hand"""
        self.cards.append(card)

    # Delegate evaluation to BlackjackEvaluator
    def get_total(self) -> int:
        """Get the total value of the hand"""
        return BlackjackEvaluator.get_total(self.cards)

    def is_soft(self) -> bool:
        """Check if hand is soft (has usable ace counted as 11)"""
        return BlackjackEvaluator.is_soft(self.cards)

    def is_blackjack(self) -> bool:
        """Check if hand is a natural blackjack"""
        return BlackjackEvaluator.is_blackjack(self.cards)

    def is_busted(self) -> bool:
        """Check if hand is busted"""
        return BlackjackEvaluator.is_busted(self.cards)

    # Dealer-specific behavior
    def get_upcard(self) -> Card:
        """Get the dealer's visible card (first card)"""
        if not self.cards:
            raise ValueError("Dealer has no cards")
        return self.cards[0]