"""Tests for PlayerHand and DealerHand business rules."""
import pytest
from casino.domain import Card, Rank, Suit
from casino.blackjack.domain import PlayerHand, DealerHand, PlayerHandResult


class TestPlayerHandBasics:
    """Test basic PlayerHand functionality."""
    
    def test_create_hand_with_bet(self):
        """Can create a hand with a bet amount."""
        hand = PlayerHand(bet=10)
        assert hand.bet == 10
        assert len(hand.cards) == 0
        assert hand.is_active is True
        assert hand.is_doubled is False
        assert hand.is_split is False
        assert hand.is_surrendered is False
    
    def test_add_card(self):
        """Can add cards to hand."""
        hand = PlayerHand(bet=10)
        card = Card(Rank.KING, Suit.HEART)
        hand.add_card(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card
    
    def test_len_returns_card_count(self):
        """len() returns number of cards."""
        hand = PlayerHand(bet=10)
        assert len(hand) == 0
        hand.add_card(Card(Rank.KING, Suit.HEART))
        assert len(hand) == 1
        hand.add_card(Card(Rank.FIVE, Suit.DIAMOND))
        assert len(hand) == 2


class TestPlayerHandEvaluation:
    """Test hand evaluation methods (delegates to evaluator)."""
    
    def test_get_total(self):
        """get_total returns correct value."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.KING, Suit.HEART))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMOND))
        assert hand.get_total() == 15
    
    def test_is_soft(self):
        """is_soft detects soft hands."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.SIX, Suit.HEART))
        assert hand.is_soft() is True
    
    def test_is_busted(self):
        """is_busted detects busted hands."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.KING, Suit.HEART))
        hand.add_card(Card(Rank.QUEEN, Suit.DIAMOND))
        hand.add_card(Card(Rank.FIVE, Suit.SPADE))
        assert hand.is_busted() is True


class TestPlayerHandIsBlackjack:
    """Test blackjack detection with split logic."""
    
    def test_natural_blackjack(self):
        """Natural blackjack (Ace + 10) is blackjack."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.HEART))
        assert hand.is_blackjack() is True
    
    def test_blackjack_with_face_cards(self):
        """Blackjack works with any face card."""
        for rank in [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING]:
            hand = PlayerHand(bet=10)
            hand.add_card(Card(Rank.ACE, Suit.SPADE))
            hand.add_card(Card(rank, Suit.HEART))
            assert hand.is_blackjack() is True
    
    def test_split_hand_not_blackjack(self):
        """Split hand with 21 is not blackjack."""
        hand = PlayerHand(bet=10, is_split=True)
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.HEART))
        assert hand.get_total() == 21
        assert hand.is_blackjack() is False
    
    def test_three_card_twenty_one_not_blackjack(self):
        """21 with 3 cards is not blackjack."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.SEVEN, Suit.SPADE))
        hand.add_card(Card(Rank.SEVEN, Suit.HEART))
        hand.add_card(Card(Rank.SEVEN, Suit.DIAMOND))
        assert hand.get_total() == 21
        assert hand.is_blackjack() is False


class TestCanDouble:
    """Test can_double business rule."""
    
    def test_can_double_with_two_cards(self):
        """Can double with exactly 2 cards."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.FIVE, Suit.HEART))
        hand.add_card(Card(Rank.SIX, Suit.DIAMOND))
        assert hand.can_double() is True
    
    def test_cannot_double_with_one_card(self):
        """Cannot double with 1 card."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.FIVE, Suit.HEART))
        assert hand.can_double() is False
    
    def test_cannot_double_with_three_cards(self):
        """Cannot double with 3+ cards."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.FIVE, Suit.HEART))
        hand.add_card(Card(Rank.THREE, Suit.DIAMOND))
        hand.add_card(Card(Rank.TWO, Suit.SPADE))
        assert hand.can_double() is False
    
    def test_can_double_regardless_of_total(self):
        """Can double regardless of hand total (rule enforcement is elsewhere)."""
        # Can double on blackjack (though engine may prevent it)
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.HEART))
        assert hand.can_double() is True


class TestCanSurrender:
    """Test can_surrender business rule."""
    
    def test_can_surrender_with_two_cards(self):
        """Can surrender with exactly 2 cards."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.TEN, Suit.HEART))
        hand.add_card(Card(Rank.SIX, Suit.DIAMOND))
        assert hand.can_surrender() is True
    
    def test_cannot_surrender_with_one_card(self):
        """Cannot surrender with 1 card."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.TEN, Suit.HEART))
        assert hand.can_surrender() is False
    
    def test_cannot_surrender_with_three_cards(self):
        """Cannot surrender with 3+ cards."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.FIVE, Suit.HEART))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMOND))
        hand.add_card(Card(Rank.SIX, Suit.SPADE))
        assert hand.can_surrender() is False


class TestCanSplit:
    """Test can_split business rule - complex value matching logic."""
    
    def test_can_split_matching_ranks(self):
        """Can split two cards of same rank."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        assert hand.can_split() is True
    
    def test_can_split_different_suits_same_rank(self):
        """Can split same rank regardless of suit."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.ACE, Suit.HEART))
        assert hand.can_split() is True
    
    def test_can_split_ten_value_cards(self):
        """Can split cards with same value even if different ranks."""
        # Ten and Jack both have value 10
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.TEN, Suit.HEART))
        hand.add_card(Card(Rank.JACK, Suit.DIAMOND))
        assert hand.can_split() is True
    
    def test_can_split_face_cards(self):
        """Can split different face cards (all value 10)."""
        # King and Queen
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.KING, Suit.HEART))
        hand.add_card(Card(Rank.QUEEN, Suit.DIAMOND))
        assert hand.can_split() is True
        
        # Jack and King
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.JACK, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.CLUB))
        assert hand.can_split() is True
    
    def test_cannot_split_different_values(self):
        """Cannot split cards with different values."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.NINE, Suit.HEART))
        hand.add_card(Card(Rank.TEN, Suit.DIAMOND))
        assert hand.can_split() is False
    
    def test_cannot_split_one_card(self):
        """Cannot split with only 1 card."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        assert hand.can_split() is False
    
    def test_cannot_split_three_cards(self):
        """Cannot split with 3+ cards."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        hand.add_card(Card(Rank.EIGHT, Suit.SPADE))
        assert hand.can_split() is False
    
    def test_cannot_split_ace_and_ten(self):
        """Cannot split Ace and Ten (different values)."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.TEN, Suit.HEART))
        assert hand.can_split() is False


class TestSplit:
    """Test split operation - complex state transformation."""
    
    def test_split_creates_two_hands(self):
        """Split creates two separate hands."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        
        hand1, hand2 = hand.split()
        
        assert isinstance(hand1, PlayerHand)
        assert isinstance(hand2, PlayerHand)
        assert hand1 is not hand2
    
    def test_split_distributes_cards(self):
        """Each new hand gets one card from the pair."""
        card1 = Card(Rank.EIGHT, Suit.HEART)
        card2 = Card(Rank.EIGHT, Suit.DIAMOND)
        hand = PlayerHand(bet=10)
        hand.add_card(card1)
        hand.add_card(card2)
        
        hand1, hand2 = hand.split()
        
        assert len(hand1.cards) == 1
        assert len(hand2.cards) == 1
        assert hand1.cards[0] == card1
        assert hand2.cards[0] == card2
    
    def test_split_preserves_bet(self):
        """Both new hands have same bet as original."""
        hand = PlayerHand(bet=25)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        
        hand1, hand2 = hand.split()
        
        assert hand1.bet == 25
        assert hand2.bet == 25
    
    def test_split_marks_hands_as_split(self):
        """Both new hands are marked as split."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        
        hand1, hand2 = hand.split()
        
        assert hand1.is_split is True
        assert hand2.is_split is True
    
    def test_split_tracks_split_rank(self):
        """Both hands track what rank was split."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.ACE, Suit.HEART))
        hand.add_card(Card(Rank.ACE, Suit.DIAMOND))
        
        hand1, hand2 = hand.split()
        
        assert hand1.split_from_rank == Rank.ACE
        assert hand2.split_from_rank == Rank.ACE
    
    def test_split_different_rank_same_value(self):
        """Split tracks first card's rank even if values match."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.KING, Suit.HEART))
        hand.add_card(Card(Rank.QUEEN, Suit.DIAMOND))
        
        hand1, hand2 = hand.split()
        
        # Both track KING since that was the first card
        assert hand1.split_from_rank == Rank.KING
        assert hand2.split_from_rank == Rank.KING
    
    def test_split_new_hands_are_active(self):
        """New hands start as active."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        
        hand1, hand2 = hand.split()
        
        assert hand1.is_active is True
        assert hand2.is_active is True
    
    def test_split_new_hands_not_doubled(self):
        """New hands are not marked as doubled."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        
        hand1, hand2 = hand.split()
        
        assert hand1.is_doubled is False
        assert hand2.is_doubled is False
    
    def test_split_raises_on_non_splittable(self):
        """Split raises ValueError if hand cannot be split."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.NINE, Suit.HEART))
        hand.add_card(Card(Rank.TEN, Suit.DIAMOND))
        
        with pytest.raises(ValueError, match="cannot be split"):
            hand.split()
    
    def test_split_raises_with_three_cards(self):
        """Split raises ValueError with 3+ cards."""
        hand = PlayerHand(bet=10)
        hand.add_card(Card(Rank.EIGHT, Suit.HEART))
        hand.add_card(Card(Rank.EIGHT, Suit.DIAMOND))
        hand.add_card(Card(Rank.EIGHT, Suit.SPADE))
        
        with pytest.raises(ValueError, match="cannot be split"):
            hand.split()


class TestDealerHand:
    """Test DealerHand functionality."""
    
    def test_create_dealer_hand(self):
        """Can create a dealer hand."""
        hand = DealerHand()
        assert len(hand.cards) == 0
        assert hand.hole_card_revealed is False
    
    def test_add_card(self):
        """Can add cards to dealer hand."""
        hand = DealerHand()
        card = Card(Rank.KING, Suit.HEART)
        hand.add_card(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card
    
    def test_get_upcard(self):
        """get_upcard returns first card."""
        hand = DealerHand()
        upcard = Card(Rank.KING, Suit.HEART)
        hole_card = Card(Rank.ACE, Suit.SPADE)
        hand.add_card(upcard)
        hand.add_card(hole_card)
        
        assert hand.get_upcard() == upcard
    
    def test_get_upcard_raises_on_empty(self):
        """get_upcard raises ValueError if no cards."""
        hand = DealerHand()
        with pytest.raises(ValueError, match="no cards"):
            hand.get_upcard()
    
    def test_dealer_evaluation_methods(self):
        """Dealer hand has same evaluation methods as player."""
        hand = DealerHand()
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.HEART))
        
        assert hand.get_total() == 21
        assert hand.is_soft() is True
        assert hand.is_blackjack() is True
        assert hand.is_busted() is False
    
    def test_dealer_blackjack_not_affected_by_split(self):
        """Dealer hand doesn't have split logic (always natural)."""
        hand = DealerHand()
        hand.add_card(Card(Rank.ACE, Suit.SPADE))
        hand.add_card(Card(Rank.KING, Suit.HEART))
        
        # Dealer always has natural blackjack with Ace+10
        assert hand.is_blackjack() is True


class TestPlayerHandResult:
    """Test PlayerHandResult enum."""
    
    def test_result_values(self):
        """Result enum has correct values."""
        assert PlayerHandResult.WIN.value == "win"
        assert PlayerHandResult.LOSE.value == "lose"
        assert PlayerHandResult.PUSH.value == "push"
        assert PlayerHandResult.SURRENDERED.value == "surrendered"
    
    def test_result_str(self):
        """Result enum converts to string."""
        assert str(PlayerHandResult.WIN) == "win"
        assert str(PlayerHandResult.LOSE) == "lose"
        assert str(PlayerHandResult.PUSH) == "push"
        assert str(PlayerHandResult.SURRENDERED) == "surrendered"

# Made with Bob
