from casino.domain import Rank
from casino.blackjack.domain import Action

from .base import DecisionStrategy, DecisionContext

class BasicStrategyDecisionStrategy(DecisionStrategy):

    _RANK_VALUES = {
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
        Rank.ACE: 11,
    }

    def decide(self, context: DecisionContext) -> Action:
        player_total = context.hand.get_total()
        dealer_upcard_value = BasicStrategyDecisionStrategy._RANK_VALUES[context.dealer_upcard.rank]

        if Action.SPLIT in context.actions:
            split_card = context.hand.cards[0]
            split_value = BasicStrategyDecisionStrategy._RANK_VALUES[split_card.rank]
            if BasicStrategyDecisionStrategy._should_split(
                    split_value=split_value, 
                    dealer_upcard_value=dealer_upcard_value, 
                    double_after_split=context.double_after_split,
                ):
                return Action.SPLIT
        
        if Action.SURRENDER in context.actions:
            if BasicStrategyDecisionStrategy._should_surrender(
                player_total=player_total, 
                dealer_upcard_value=dealer_upcard_value,
                num_decks=context.num_decks,
                dealer_hits_soft_17=context.dealer_hits_soft_17,
            ):
                return Action.SURRENDER

        if context.hand.is_soft():
            return BasicStrategyDecisionStrategy._soft_hand(
                player_total=player_total, 
                dealer_upcard_value=dealer_upcard_value, 
                num_decks=context.num_decks,
                dealer_hits_soft_17=context.dealer_hits_soft_17,
                can_double=Action.DOUBLE in context.actions,
            )

        return BasicStrategyDecisionStrategy._hard_hand(
            player_total=player_total, 
            dealer_upcard_value=dealer_upcard_value, 
            num_decks=context.num_decks,
            dealer_hits_soft_17=context.dealer_hits_soft_17,
            can_double=Action.DOUBLE in context.actions,
            dealer_peak=context.dealer_peak,
        )

    @staticmethod
    def _should_split(
        split_value: int, 
        dealer_upcard_value: int, 
        double_after_split: bool,
    )-> bool:

        if split_value in [8, 11]:
            return True

        if split_value == 9:
            return dealer_upcard_value not in [11, 10, 7]

        if split_value == 7:
            return 2 <= dealer_upcard_value <= 7

        if split_value == 6:
            return (3 <= dealer_upcard_value <= 6) or (dealer_upcard_value == 2 and double_after_split)

        if split_value == 4 and double_after_split:
            return 4 <= dealer_upcard_value <= 5

        if split_value in [2, 3] and double_after_split:
            return 2 <= dealer_upcard_value <= 6

        return False

    @staticmethod
    def _should_surrender(
        player_total: int, 
        dealer_upcard_value: int, 
        num_decks: int,
        dealer_hits_soft_17: bool,
    ) -> bool:
        
        if player_total == 17 and dealer_upcard_value == 11 and dealer_hits_soft_17:
            return True

        if player_total == 16:
            if 10 <= dealer_upcard_value <= 11:
                return True
            if dealer_upcard_value == 9 and num_decks >= 4:
                return True

        if player_total == 15:
            if dealer_upcard_value == 10 and num_decks >= 2:
                return True
            if dealer_upcard_value == 11 and dealer_hits_soft_17:
                return True

        return False

    @staticmethod
    def _soft_hand(
        player_total: int, 
        dealer_upcard_value: int, 
        num_decks: int,
        dealer_hits_soft_17: bool,
        can_double: bool,
    )-> Action:

        if player_total > 19:
            return Action.STAND
        
        if player_total == 19:
            if can_double and dealer_upcard_value == 6 and (dealer_hits_soft_17 or num_decks == 1):
                return Action.DOUBLE
            return Action.STAND
        
        if player_total == 18:
            if can_double and 3 <= dealer_upcard_value <= 6:
                return Action.DOUBLE
            if can_double and dealer_upcard_value == 2 and dealer_hits_soft_17:
                return Action.DOUBLE
            
            if 2 <= dealer_upcard_value <= 8:
                return Action.STAND
            if dealer_upcard_value == 11 and num_decks == 1 and not dealer_hits_soft_17:
                return Action.STAND

        if can_double:
            if player_total == 17:
                if 3 <= dealer_upcard_value <= 6:
                    return Action.DOUBLE
                if dealer_upcard_value == 2 and num_decks == 1:
                    return Action.DOUBLE

            if player_total == 16:
                if 4 <= dealer_upcard_value <= 6:
                    return Action.DOUBLE
            
            if player_total == 15:
                if 4 <= dealer_upcard_value <= 6:
                    return Action.DOUBLE

            if player_total == 14:
                if 5 <= dealer_upcard_value <= 6:
                    return Action.DOUBLE
                if dealer_upcard_value == 4 and num_decks <= 2 and dealer_hits_soft_17:
                    return Action.DOUBLE
                if dealer_upcard_value == 4 and num_decks == 1:
                    return Action.DOUBLE

            if player_total == 13:
                if 5 <= dealer_upcard_value <= 6:
                    return Action.DOUBLE
                if dealer_upcard_value == 4 and num_decks == 1:
                    return Action.DOUBLE

        return Action.HIT

    @staticmethod
    def _hard_hand(
        player_total: int, 
        dealer_upcard_value: int, 
        num_decks: int,
        dealer_hits_soft_17: bool,
        can_double: bool,
        dealer_peak: bool,
    )-> Action:

        if player_total >= 17:
            return Action.STAND

        if 13 <= player_total <= 16 and dealer_upcard_value <= 6:
            return Action.STAND

        if player_total == 12 and 4 <= dealer_upcard_value <= 6:
            return Action.STAND

        # easier to write this as an exception, then none of the doubling rules depends on the dealer_peak variable
        if not dealer_peak:
            if player_total == 11 and 10 <= dealer_upcard_value <= 11:
                return Action.HIT

        if can_double:
            if player_total == 11:
                if dealer_upcard_value <= 10:
                    return Action.DOUBLE
                if dealer_upcard_value == 11 and (num_decks <= 2 or dealer_hits_soft_17):
                    return Action.DOUBLE

            if player_total == 10 and dealer_upcard_value <= 9:
                return Action.DOUBLE
            
            if player_total == 9:
                if 3 <= dealer_upcard_value <= 6:
                    return Action.DOUBLE
                if dealer_upcard_value == 2 and num_decks <= 2:
                    return Action.DOUBLE

            if player_total == 8 and 5 <= dealer_upcard_value <= 6 and num_decks == 1:
                return Action.DOUBLE

        return Action.HIT
    
    