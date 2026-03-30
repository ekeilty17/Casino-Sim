
from typing import List, Set

from casino.dealing import DealingDevice
from casino.blackjack.domain import (
    Action,
    Player,
    PlayerHand, DealerHand, PlayerHandResult,
    Limits,
    Rules, SurrenderRule,
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

        self.state = None

    def run(self):
        for player in self.players:
            print(player)
        print()
        table_state = self.initialize_table_state()
        print(table_state)
        
        return
        table_state = self.run_round(table_state)

        return
        self.payout(round_results)

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

    def run_round(self, table_state: TableState) -> TableState:

        if self.rules.dealer_peak:
            if table_state.dealer_hand.is_blackjack():
                self.evaluate_hand_results()       # TODO better name and implement

        for spot in table_state.spots:
            self.player_action(self, spot)          # TODO better name and implement

        self.dealer_action(self)                    # TODO better name and implement

        for spot in table_state.spots:
            for player_hand in spot.hands:
                self.hand_result(player_hand, self.dealer_hand)

    def player_action(self, spot: Spot):
        while all(hand.is_active for hand in spot.hands):
            for hand in spot.hands:
                if not hand.is_active:
                    continue
                
                actions = self.get_allowed_actions(hand)
                decision_context = DecisionContext(actions=actions)
                action = spot.player.decision_strategy.decide(decision_context)

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
                actions=[Action.HIT, Action.STAND],
                dealer_hits_soft_17=self.rules.dealer_hits_soft_17
            )
            
            # Get dealer's decision
            action = self.dealer_strategy.decide(context)
            
            if action == Action.STAND:
                break
            
            # Dealer hits - deal one card
            cards = self.dealing_device.deal(1)
            table_state.dealer_hand.add_card(cards[0])

    def hand_result(self, player_cards: Cards, dealer_cards: Cards) -> PlayerHandResult:
        if dealer_cards.is_blackjack():
            return PlayerHandResult.LOSE
        if self.rules.dealer_peak and player_cards.is_blackjack():
            return PlayerHandResult.WIN
        
        if player_cards.is_busted():
            return PlayerHandResult.LOSE
        if dealer_cards.is_busted():
            return PlayerHandResult.WIN
        
        if dealer_cards == player_cards:
            return PlayerHandResult.PUSH
        if dealer_cards > player_cards:
            return PlayerHandResult.LOSE
        return PlayerHandResult.WIN

    def payout(self, round_results):
        pass

    def get_allowed_actions(self, hand: PlayerHand) -> Set[Action]:
        allowed_actions: Set[Action] = set([Action.HIT, Action.STAND])
        
        if hand.can_surrender() and self.rules.surrender != SurrenderRule.NEVER:
            allowed_actions.add(Action.SURRENDER)

        if hand.can_double():
            # TODO: check for DAS rule and aces exception
            # TODO: also need to check if they have enough money
            allowed_actions.add(Action.DOUBLE)

        if hand.can_split():
            # TODO: check for split limit
            # TODO: also need to check if they have enough money
            allowed_actions.add(Action.SPLIT)
    
        return allowed_actions