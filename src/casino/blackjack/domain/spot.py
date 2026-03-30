from dataclasses import dataclass, field
from typing import List, Any, Optional

from .hand import PlayerHand
from .player import Player

@dataclass
class Spot:
    """
    Represents a betting spot at the blackjack table.
    
    A spot links a player to their hand(s). It manages the split action
    which requires both hand state and player context (bankroll validation).
    """
    player: Player
    hands: List[PlayerHand] = field(default_factory=list)
    # side_bets: Optional[Any] = None      # TODO later

    def split(self, hand_index: int) -> None:
        """
        Split the specified hand into two separate hands.
        
        Validates player has sufficient bankroll for the additional bet,
        delegates card splitting to PlayerHand, and updates the spot's hand list.
        
        Args:
            hand_index: Index of the hand to split
            
        Raises:
            ValueError: If player lacks funds or hand cannot be split
            IndexError: If hand_index is invalid
        """
        hand = self.hands[hand_index]
        
        # Validate player has sufficient bankroll for additional bet
        if self.player.bankroll < hand.bet:
            raise ValueError(
                f"Cannot split hand {hand_index}: insufficient bankroll "
                f"(hand bet = {hand.bet}, player bankroll = {self.player.bankroll})"
            )
        
        # Delegate card splitting to hand (may raise ValueError if not splittable)
        new_hand1, new_hand2 = hand.split()
        
        # Deduct additional bet from bankroll (only after validation succeeds)
        self.player.place_bet(hand.bet)
        
        # Replace original hand with two new hands
        self.hands[hand_index:hand_index + 1] = [new_hand1, new_hand2]