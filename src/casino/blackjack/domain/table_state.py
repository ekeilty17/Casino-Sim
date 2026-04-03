from dataclasses import dataclass, field
from typing import List, Any, Optional

from .hand import DealerHand
from .spot import Spot
from .evaluator import BlackjackEvaluator


@dataclass
class TableState:
    dealer_hand: DealerHand
    spots: List[Spot] = field(default_factory=list)

    def display(self) -> str:
        """
        Generate a human-readable terminal display of the table state.
        
        This is intended for debugging purposes. In production, consider:
        - Using a dedicated display/formatting module <-- TODO definitely let's do this eventually
        - Integrating with logging frameworks
        - Using rich library for advanced terminal formatting
        
        Returns:
            Formatted string representation of the table state
        """
        lines = []
        lines.append("=" * 80)
        lines.append("BLACKJACK TABLE STATE".center(80))
        lines.append("=" * 80)
        
        # Display dealer's hand
        lines.append("")
        lines.append("DEALER:")
        lines.append(self._format_dealer_hand())
        
        # Display each player spot
        lines.append("")
        lines.append("PLAYERS:")
        lines.append("-" * 80)
        
        if not self.spots:
            lines.append("  (No players at table)")
        else:
            for i, spot in enumerate(self.spots, 1):
                lines.append(self._format_spot(i, spot))
                if i < len(self.spots):
                    lines.append("-" * 80)
        
        lines.append("=" * 80)
        return "\n".join(lines)
    
    def _format_dealer_hand(self) -> str:
        """Format the dealer's hand for display."""
        cards = self.dealer_hand.cards
        
        if not cards:
            return "  No cards"
        
        # Show hole card as [??] if not revealed
        if len(cards) >= 2 and not self.dealer_hand.hole_card_revealed:
            visible_cards = [str(cards[0])] + ["[??]"] * (len(cards) - 1)
            cards_str = " ".join(visible_cards)
            upcard_value = BlackjackEvaluator.get_card_value(cards[0].rank)
            return f"  Cards: {cards_str}  (Upcard: {upcard_value})"
        
        # All cards visible
        cards_str = " ".join(str(card) for card in cards)
        total = self.dealer_hand.get_total()
        soft_indicator = " (soft)" if self.dealer_hand.is_soft() else ""
        
        status = ""
        if self.dealer_hand.is_blackjack():
            status = " ★ BLACKJACK ★"
        elif self.dealer_hand.is_busted():
            status = " ✗ BUST"
        
        return f"  Cards: {cards_str}  Total: {total}{soft_indicator}{status}"
    
    def _format_spot(self, spot_number: int, spot: Spot) -> str:
        """Format a player spot with all hands for display."""
        lines = []
        player = spot.player
        
        # Player header
        lines.append(f"  Spot {spot_number}: {player.name} (ID: {player.player_id})")
        lines.append(f"  Bankroll: ${player.bankroll}")
        
        # Display each hand
        if not spot.hands:
            lines.append("    No hands")
        else:
            for hand_idx, hand in enumerate(spot.hands, 1):
                hand_label = f"Hand {hand_idx}" if len(spot.hands) > 1 else "Hand"
                lines.append(f"    {hand_label}:")
                lines.append(self._format_player_hand(hand))
        
        return "\n".join(lines)
    
    def _format_player_hand(self, hand) -> str:
        """Format a single player hand for display."""
        if not hand.cards:
            return "      No cards"
        
        cards_str = " ".join(str(card) for card in hand.cards)
        total = hand.get_total()
        soft_indicator = " (soft)" if hand.is_soft() else ""
        
        # Build status indicators
        status_parts = []
        if hand.is_blackjack():
            status_parts.append("★ BLACKJACK ★")
        elif hand.is_busted():
            status_parts.append("✗ BUST")
        
        if hand.is_doubled:
            status_parts.append("DOUBLED")
        if hand.is_surrendered:
            status_parts.append("SURRENDERED")
        if hand.is_split:
            status_parts.append(f"SPLIT from {hand.split_from_rank.symbol if hand.split_from_rank else '?'}")
        if not hand.is_active:
            status_parts.append("INACTIVE")
        
        status = f" [{', '.join(status_parts)}]" if status_parts else ""
        
        return f"      Cards: {cards_str}  Total: {total}{soft_indicator}  Bet: ${hand.bet}{status}"