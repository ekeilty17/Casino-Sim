
from typing import List, Set

from casino.domain import Card, Rank
from casino.dealing import DealingDevice
from casino.blackjack.domain import (
    Action,
    Player,
    PlayerHand, DealerHand, PlayerHandResult,
    Limits,
    Rules, SurrenderRule, DoubleRule,
    Spot,
    TableState,
)
from casino.blackjack.betting import BettingContext
from casino.blackjack.decision import DecisionContext, DealerDecisionStrategy

class Engine:

    def __init__(
        self,
        dealing_device: DealingDevice,
        players: List[Player],
        rules: Rules,
        limits: Limits,
    ):
        self.dealing_device = dealing_device
        self.players = players
        self.rules = rules
        self.limits = limits
        self.dealer_strategy = DealerDecisionStrategy()

    def run(self):
        table_state = self.initialize_table_state()
        self.run_round(table_state)

    def initialize_table_state(self) -> TableState:
        spots: List[Spot] = []

        # Deal to players
        for player in self.players:
            betting_context = BettingContext(
                bankroll=player.bankroll,
                min_bet=self.limits.min_bet,
                max_bet=self.limits.max_bet,
            )

            bet = player.place_bet(context=betting_context)
            if bet > 0:
                initial_cards = list(self.dealing_device.deal(2))
                hand = PlayerHand(bet=bet, cards=initial_cards)
                spot = Spot(player=player, hands=[hand])
                spots.append(spot)
            else:
                # Skip players who are not betting
                spots.append(Spot(player=player, hands=[]))

        # Deal to dealer
        dealer_cards = list(self.dealing_device.deal(2 if self.rules.dealer_peak else 1))
        dealer_hand = DealerHand(cards=dealer_cards)

        return TableState(dealer_hand=dealer_hand, spots=spots)

    def run_round(self, table_state: TableState):

        if self.rules.dealer_peak:
            # TODO: Implement Early Surrender
            # There might be other types of early surrender where it's only against dealer 10 or something
            # idk it's not even a rule most casinos implement anymore, so I'll leave this as a future enhancement
            if self.rules.surrender == SurrenderRule.EARLY:
                # TODO: ask for surrender
                pass

            dealer_upcard: Card = table_state.dealer_hand.get_upcard()
            if dealer_upcard.rank == Rank.ACE:
                # TODO: ask for insurance / even money
                pass

            if table_state.dealer_hand.is_blackjack():
                # No player actions allowed
                self.compare_and_payout_hands(table_state)
                return table_state

        for spot in table_state.spots:
            self.player_action(spot, table_state.dealer_hand)

        table_state.dealer_hand.hole_card_revealed = True
        self.dealer_action(table_state)

        self.compare_and_payout_hands(table_state)
        return table_state

    def player_action(self, spot: Spot, dealer_hand: DealerHand):
        while all(hand.is_active for hand in spot.hands):
            for hand_index in range(len(spot.hands)):
                hand: PlayerHand = spot.hands[hand_index]
                if not hand.is_active:
                    continue
                
                if len(hand) == 0:
                    raise ValueError("Unexpected hand length of 0")
                if len(hand) == 1:
                    # This occurs on splits
                    hand.add_card(self.dealing_device.next_card())

                actions = self.get_allowed_actions(hand, spot)
                if len(actions) == 1:
                    action = actions.pop()
                else:
                    decision_context = DecisionContext(
                        dealer_upcard=dealer_hand.get_upcard(),
                        hand=hand,
                        actions=actions,
                        dealer_hits_soft_17=self.rules.dealer_hits_soft_17
                    )
                    action = spot.player.decision_strategy.decide(decision_context)

                if action == Action.STAND:
                    hand.is_active = False
                
                elif action == Action.HIT:
                    hand.add_card(self.dealing_device.next_card())
                
                elif action == Action.SURRENDER:
                    hand.is_active = False
                    hand.is_surrendered = True
                
                elif action == Action.DOUBLE:
                    if spot.player.bankroll < hand.bet:
                        raise ValueError(
                            f"Cannot double hand {hand_index}: insufficient bankroll "
                            f"(hand bet = {hand.bet}, player bankroll = {spot.player.bankroll})"
                        )
                    spot.player.place_bet(hand.bet)
                    hand.add_card(self.dealing_device.next_card())
                    hand.is_doubled = True
                    hand.is_active = False
                
                elif action == Action.SPLIT:
                    spot.split(hand_index)

                    # Break so that we reloop through the hand indices
                    break
                
                else:
                    raise TypeError(f"Unexpected action type {action}")

    def dealer_action(self, table_state: TableState):
        """
        Execute dealer's turn using DealerDecisionStrategy.
        Dealer draws cards until strategy says to stand or busts.
        """
        while not table_state.dealer_hand.is_busted():
            # Create decision context for dealer
            context = DecisionContext(
                dealer_upcard=table_state.dealer_hand.get_upcard(),
                hand=table_state.dealer_hand,
                actions={Action.HIT, Action.STAND},
                dealer_hits_soft_17=self.rules.dealer_hits_soft_17
            )
            
            # Get dealer's decision
            action = self.dealer_strategy.decide(context)
            
            if action == Action.STAND:
                break
            
            # Dealer hits
            table_state.dealer_hand.add_card(self.dealing_device.next_card())

    def hand_result(self, player_hand: PlayerHand, dealer_hand: DealerHand) -> PlayerHandResult:
        if player_hand.is_surrendered:
            return PlayerHandResult.SURRENDERED
        
        if self.rules.dealer_peak:
            if dealer_hand.is_blackjack():
                return PlayerHandResult.LOSE
            if player_hand.is_blackjack():
                return PlayerHandResult.WIN
        
        if player_hand.is_busted():
            return PlayerHandResult.LOSE
        if dealer_hand.is_busted():
            return PlayerHandResult.WIN

        if dealer_hand.get_total() == player_hand.get_total():
            return PlayerHandResult.PUSH
        if dealer_hand.get_total() > player_hand.get_total():
            return PlayerHandResult.LOSE
        return PlayerHandResult.WIN

    def compare_and_payout_hands(self, table_state: TableState): 
        for spot in table_state.spots:
            for hand in spot.hands:
                result = self.hand_result(hand, table_state.dealer_hand)
                self.payout(spot.player, hand.bet, result)

    def payout(self, player: Player, bet: int, result: PlayerHandResult):
        if result == PlayerHandResult.WIN:
            player.receive_payout(2 * bet)
        
        if result == PlayerHandResult.PUSH:
            player.receive_payout(bet)
        
        if result == PlayerHandResult.SURRENDERED:
            player.receive_payout(bet // 2)

    def get_allowed_actions(self, hand: PlayerHand, spot: Spot) -> Set[Action]:
        """
        Determine which actions are allowed for a hand based on game rules and context.
        
        Checks hand state, game rules, and player resources to determine valid actions.
        
        Args:
            hand: The player hand to check
            spot: The spot containing the player and their hands
            
        Returns:
            Set of allowed actions for this hand
        """
        allowed_actions: Set[Action] = {Action.HIT, Action.STAND}
        
        # Surrender - check hand state and rules
        if hand.can_surrender():
            if self._can_surrender_with_rules(hand, spot):
                allowed_actions.add(Action.SURRENDER)
        
        # Double - check hand state, then apply rules
        if hand.can_double():
            if self._can_double_with_rules(hand, spot):
                allowed_actions.add(Action.DOUBLE)
        
        # Split - check hand state, then apply rules
        if hand.can_split():
            if self._can_split_with_rules(hand, spot):
                allowed_actions.add(Action.SPLIT)
        
        # Special rule: No hit after split aces
        if hand.split_from_rank == Rank.ACE and not self.rules.hit_after_split_aces:
            # Force STAND if just received second card
            allowed_actions = {Action.STAND}
        
        return allowed_actions
    
    def _can_surrender_with_rules(self, hand: PlayerHand, spot: Spot) -> bool:
        """
        Check if surrendering is allowed by game rules and player resources.
        
        Args:
            hand: The hand to check
            spot: The spot containing the player
            
        Returns:
            True if surrendering is allowed, False otherwise
        """
        return self.rules.surrender != SurrenderRule.NEVER

         
    def _can_double_with_rules(self, hand: PlayerHand, spot: Spot) -> bool:
        """
        Check if doubling is allowed by game rules and player resources.
        
        Args:
            hand: The hand to check
            spot: The spot containing the player
            
        Returns:
            True if doubling is allowed, False otherwise
        """
        # Check double after split rule
        if hand.is_split and not self.rules.double_after_split:
            return False
        
        # Check if doubling is allowed at all
        if self.rules.double == DoubleRule.NEVER:
            return False
        
        # Check specific totals rule
        if self.rules.double == DoubleRule.SPECIFIC_TOTALS:
            if hand.get_total() not in self.rules.double_allowed_totals:
                return False
        
        # Check player has sufficient bankroll
        if spot.player.bankroll < hand.bet:
            return False
        
        return True
    
    def _can_split_with_rules(self, hand: PlayerHand, spot: Spot) -> bool:
        """
        Check if splitting is allowed by game rules and player resources.
        
        Args:
            hand: The hand to check
            spot: The spot containing the player and their hands
            
        Returns:
            True if splitting is allowed, False otherwise
        """
        # Check resplit aces rule
        if hand.split_from_rank == Rank.ACE and not self.rules.resplit_aces:
            return False
        
        # Check max splits rule
        if self.rules.max_splits is not None:
            # Count how many times we've already split at this spot
            split_count = sum(1 for h in spot.hands if h.is_split)
            if split_count >= self.rules.max_splits:
                return False
        
        # Check player has sufficient bankroll for additional bet
        if spot.player.bankroll < hand.bet:
            return False
        
        return True