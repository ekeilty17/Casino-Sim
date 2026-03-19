from enum import Enum
from typing import List

from core.player import Player
from card_dealing_devices.card_dealing_device import CardDealingDevice
from blackjack.core.rules import BlackjackRules, SurrenderRule
from blackjack.core.table import BlackjackTable
from blackjack.core.hand import BlackJackHand
from blackjack.core.action import BlackJackAction

class BlackJackHandResult(Enum):
    WIN     = "win"
    LOSE    = "lose"
    PUSH    = "push"

    def __str__(self):
        return self.value

class BlackJackEngine:

    def __init__(
        self,
        players: List[Player],
        card_dealing_device: CardDealingDevice,
        rules: BlackjackRules,
        table: BlackjackTable,
    ):  
        self.players = players
        self.card_dealing_device = card_dealing_device
        self.rules = rules
        self.table = table
        self.dealer = None

        self.state = None

    def run(self):

        bets: List[int] = self.accept_bets()
        
        active_players: List[Player] = []
        round_results = self.run_round(active_players)

        self.payout(round_results)

    def run_round(self, players: List[Player]):
        self.deal(players)

        if self.rules.dealer_peak:
            self.check_dealer_blackjack()

        for player in players:
            self.player_action(self, player)

        self.dealer_action(self)

        for player in players:
            self.determine_winner(player)


    def accept_bets(self) -> List[int]:
        pass

    def deal(self, players: List[Player]):
        pass

    def check_dealer_blackjack(self):
        pass

    def player_action(self, player: Player):
        pass

    def dealer_action(self):
        pass

    def hand_result(self, player: Player) -> BlackJackHandResult:
        if self.dealer.hand.is_blackjack():
            return BlackJackHandResult.LOSE
        if self.rules.dealer_peak and player.hand.is_blackjack():
            return BlackJackHandResult.WIN
        
        if player.hand.is_busted():
            return BlackJackHandResult.LOSE
        if self.dealer.hand.is_busted():
            return BlackJackHandResult.WIN
        
        if self.dealer.hand == player.hand:
            return BlackJackHandResult.PUSH
        if self.dealer.hand > player.hand:
            return BlackJackHandResult.LOSE
        return BlackJackHandResult.WIN

    def payout(self, round_results):
        pass

    def get_allowed_actions(self, hand: BlackJackHand):
        allowed_actions: List[BlackJackAction] = [BlackJackAction.HIT, BlackJackAction.STAND]
        
        if len(hand) == 2:
            allowed_actions.append(BlackJackAction.DOUBLE)

            if self.rules.surrender != SurrenderRule.NEVER:
                allowed_actions.append(BlackJackAction.SURRENDER)

            if hand.is_splittable():
                allowed_actions.append(BlackJackAction.SPLIT)
    
        return allowed_actions