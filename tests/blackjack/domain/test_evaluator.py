"""Tests for BlackjackEvaluator - core card evaluation logic."""
import pytest
from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import BlackjackEvaluator


class TestGetCardValue:
    """Test getting base card values."""
    
    def test_ace_value(self):
        """Ace has base value of 1."""
        assert BlackjackEvaluator.get_card_value(Rank.ACE) == 1
    
    def test_number_cards(self):
        """Number cards have their face value."""
        assert BlackjackEvaluator.get_card_value(Rank.TWO) == 2
        assert BlackjackEvaluator.get_card_value(Rank.THREE) == 3
        assert BlackjackEvaluator.get_card_value(Rank.FOUR) == 4
        assert BlackjackEvaluator.get_card_value(Rank.FIVE) == 5
        assert BlackjackEvaluator.get_card_value(Rank.SIX) == 6
        assert BlackjackEvaluator.get_card_value(Rank.SEVEN) == 7
        assert BlackjackEvaluator.get_card_value(Rank.EIGHT) == 8
        assert BlackjackEvaluator.get_card_value(Rank.NINE) == 9
    
    def test_ten_value(self):
        """Ten has value of 10."""
        assert BlackjackEvaluator.get_card_value(Rank.TEN) == 10
    
    def test_face_cards(self):
        """Face cards all have value of 10."""
        assert BlackjackEvaluator.get_card_value(Rank.JACK) == 10
        assert BlackjackEvaluator.get_card_value(Rank.QUEEN) == 10
        assert BlackjackEvaluator.get_card_value(Rank.KING) == 10


class TestGetCardValues:
    """Test getting values for multiple cards."""
    
    def test_empty_list(self):
        """Empty list returns empty list."""
        assert BlackjackEvaluator.get_card_values([]) == []
    
    def test_single_card(self):
        """Single card returns list with one value."""
        cards = [Card(Rank.FIVE, Suit.HEART)]
        assert BlackjackEvaluator.get_card_values(cards) == [5]
    
    def test_multiple_cards(self):
        """Multiple cards return list of values."""
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.KING, Suit.HEART),
            Card(Rank.FIVE, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.get_card_values(cards) == [1, 10, 5]
    
    def test_face_cards_all_ten(self):
        """Different face cards all return 10."""
        cards = [
            Card(Rank.JACK, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
            Card(Rank.KING, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.get_card_values(cards) == [10, 10, 10]


class TestGetTotal:
    """Test calculating hand totals with soft ace logic."""
    
    def test_empty_hand(self):
        """Empty hand has total of 0."""
        assert BlackjackEvaluator.get_total([]) == 0
    
    def test_hard_hand_no_ace(self):
        """Hard hand without ace."""
        cards = [Card(Rank.SEVEN, Suit.HEART), Card(Rank.NINE, Suit.DIAMOND)]
        assert BlackjackEvaluator.get_total(cards) == 16
    
    def test_soft_ace_counted_as_eleven(self):
        """Ace counted as 11 when total is 11 or less."""
        # Ace + 5 = 16 (soft)
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]
        assert BlackjackEvaluator.get_total(cards) == 16
    
    def test_soft_ace_with_ten(self):
        """Ace + 10 = 21 (blackjack)."""
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
        assert BlackjackEvaluator.get_total(cards) == 21
    
    def test_ace_counted_as_one_when_would_bust(self):
        """Ace counted as 1 when counting as 11 would bust."""
        # Ace + 7 + 8 = 16 (ace as 1)
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.SEVEN, Suit.HEART),
            Card(Rank.EIGHT, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.get_total(cards) == 16
    
    def test_multiple_aces_only_one_soft(self):
        """Only one ace can be counted as 11."""
        # Ace + Ace = 12 (one as 11, one as 1)
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.ACE, Suit.HEART)]
        assert BlackjackEvaluator.get_total(cards) == 12
    
    def test_multiple_aces_all_hard(self):
        """Multiple aces all counted as 1 when necessary."""
        # Ace + Ace + 9 = 11 (both aces as 1)
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.ACE, Suit.HEART),
            Card(Rank.NINE, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.get_total(cards) == 11
    
    def test_three_aces(self):
        """Three aces: one soft, two hard."""
        # Ace + Ace + Ace = 13 (one as 11, two as 1)
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.ACE, Suit.HEART),
            Card(Rank.ACE, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.get_total(cards) == 13
    
    def test_busted_hand(self):
        """Hand that busts."""
        cards = [
            Card(Rank.KING, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
            Card(Rank.FIVE, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.get_total(cards) == 25


class TestIsSoft:
    """Test detecting soft hands (usable ace counted as 11)."""
    
    def test_no_ace_is_not_soft(self):
        """Hand without ace is not soft."""
        cards = [Card(Rank.SEVEN, Suit.HEART), Card(Rank.NINE, Suit.DIAMOND)]
        assert BlackjackEvaluator.is_soft(cards) is False
    
    def test_ace_with_low_card_is_soft(self):
        """Ace with low card is soft."""
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.FIVE, Suit.HEART)]
        assert BlackjackEvaluator.is_soft(cards) is True
    
    def test_ace_with_ten_is_soft(self):
        """Ace with 10 is soft (blackjack)."""
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
        assert BlackjackEvaluator.is_soft(cards) is True
    
    def test_ace_that_would_bust_is_not_soft(self):
        """Ace that must be counted as 1 is not soft."""
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.SEVEN, Suit.HEART),
            Card(Rank.EIGHT, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.is_soft(cards) is False
    
    def test_multiple_aces_can_be_soft(self):
        """Multiple aces can still be soft if total allows."""
        # Ace + Ace = 12 (soft)
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.ACE, Suit.HEART)]
        assert BlackjackEvaluator.is_soft(cards) is True
    
    def test_soft_hand_becomes_hard_after_hit(self):
        """Soft hand becomes hard when ace must be counted as 1."""
        # Ace + 5 + 7 = 13 (hard)
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.FIVE, Suit.HEART),
            Card(Rank.SEVEN, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.is_soft(cards) is False
    
    def test_empty_hand_is_not_soft(self):
        """Empty hand is not soft."""
        assert BlackjackEvaluator.is_soft([]) is False


class TestIsBlackjack:
    """Test detecting natural blackjack (21 with 2 cards)."""
    
    def test_ace_and_ten_is_blackjack(self):
        """Ace + 10 is blackjack."""
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.TEN, Suit.HEART)]
        assert BlackjackEvaluator.is_blackjack(cards) is True
    
    def test_ace_and_face_card_is_blackjack(self):
        """Ace + face card is blackjack."""
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
        assert BlackjackEvaluator.is_blackjack(cards) is True
        
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.QUEEN, Suit.HEART)]
        assert BlackjackEvaluator.is_blackjack(cards) is True
        
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.JACK, Suit.HEART)]
        assert BlackjackEvaluator.is_blackjack(cards) is True
    
    def test_order_does_not_matter(self):
        """Order of cards doesn't matter for blackjack."""
        cards1 = [Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
        cards2 = [Card(Rank.KING, Suit.HEART), Card(Rank.ACE, Suit.SPADE)]
        assert BlackjackEvaluator.is_blackjack(cards1) is True
        assert BlackjackEvaluator.is_blackjack(cards2) is True
    
    def test_twenty_one_with_three_cards_is_not_blackjack(self):
        """21 with 3+ cards is not blackjack."""
        cards = [
            Card(Rank.SEVEN, Suit.SPADE),
            Card(Rank.SEVEN, Suit.HEART),
            Card(Rank.SEVEN, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.is_blackjack(cards) is False
    
    def test_two_cards_not_twenty_one_is_not_blackjack(self):
        """Two cards that don't total 21 is not blackjack."""
        cards = [Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
        assert BlackjackEvaluator.is_blackjack(cards) is False
    
    def test_empty_hand_is_not_blackjack(self):
        """Empty hand is not blackjack."""
        assert BlackjackEvaluator.is_blackjack([]) is False
    
    def test_single_card_is_not_blackjack(self):
        """Single card is not blackjack."""
        cards = [Card(Rank.ACE, Suit.SPADE)]
        assert BlackjackEvaluator.is_blackjack(cards) is False


class TestIsBusted:
    """Test detecting busted hands (over 21)."""
    
    def test_total_under_twenty_one_not_busted(self):
        """Hand under 21 is not busted."""
        cards = [Card(Rank.KING, Suit.SPADE), Card(Rank.NINE, Suit.HEART)]
        assert BlackjackEvaluator.is_busted(cards) is False
    
    def test_total_exactly_twenty_one_not_busted(self):
        """Hand exactly 21 is not busted."""
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
        assert BlackjackEvaluator.is_busted(cards) is False
    
    def test_total_over_twenty_one_is_busted(self):
        """Hand over 21 is busted."""
        cards = [
            Card(Rank.KING, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
            Card(Rank.FIVE, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.is_busted(cards) is True
    
    def test_soft_hand_cannot_bust(self):
        """Soft hand with ace cannot bust."""
        # Ace + King = 21 (soft)
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.KING, Suit.HEART)]
        assert BlackjackEvaluator.is_busted(cards) is False
    
    def test_ace_prevents_bust_when_counted_as_one(self):
        """Ace counted as 1 prevents bust."""
        # Ace + 7 + 8 = 16 (not busted)
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.SEVEN, Suit.HEART),
            Card(Rank.EIGHT, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.is_busted(cards) is False
    
    def test_empty_hand_not_busted(self):
        """Empty hand is not busted."""
        assert BlackjackEvaluator.is_busted([]) is False
    
    def test_barely_busted(self):
        """Hand with 22 is busted."""
        cards = [
            Card(Rank.KING, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
            Card(Rank.TWO, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.is_busted(cards) is True
    
    def test_heavily_busted(self):
        """Hand well over 21 is busted."""
        cards = [
            Card(Rank.KING, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
            Card(Rank.JACK, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.is_busted(cards) is True


class TestEdgeCases:
    """Test edge cases and complex scenarios."""
    
    def test_four_aces(self):
        """Four aces: one soft, three hard = 14."""
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.ACE, Suit.HEART),
            Card(Rank.ACE, Suit.DIAMOND),
            Card(Rank.ACE, Suit.CLUB),
        ]
        assert BlackjackEvaluator.get_total(cards) == 14
        assert BlackjackEvaluator.is_soft(cards) is False  # Total > 11
        assert BlackjackEvaluator.is_busted(cards) is False
    
    def test_soft_seventeen(self):
        """Ace + 6 = soft 17."""
        cards = [Card(Rank.ACE, Suit.SPADE), Card(Rank.SIX, Suit.HEART)]
        assert BlackjackEvaluator.get_total(cards) == 17
        assert BlackjackEvaluator.is_soft(cards) is True
    
    def test_soft_twenty_one_not_blackjack(self):
        """Soft 21 with 3+ cards is not blackjack."""
        # Ace + 5 + 5 = 21 (soft)
        cards = [
            Card(Rank.ACE, Suit.SPADE),
            Card(Rank.FIVE, Suit.HEART),
            Card(Rank.FIVE, Suit.DIAMOND),
        ]
        assert BlackjackEvaluator.get_total(cards) == 21
        assert BlackjackEvaluator.is_soft(cards) is False  # Total > 11
        assert BlackjackEvaluator.is_blackjack(cards) is False
    
    def test_all_face_cards_different(self):
        """Different face cards all valued at 10."""
        cards = [
            Card(Rank.JACK, Suit.SPADE),
            Card(Rank.QUEEN, Suit.HEART),
        ]
        assert BlackjackEvaluator.get_total(cards) == 20
        assert BlackjackEvaluator.get_card_values(cards) == [10, 10]

# Made with Bob
