import random
from re import S
from typing import List

from casino.roulette.domain.bet import BetCatalog

from .domain import RouletteColor, RouletteNumber, RouletteTable, Rules, Limits, RouletteWheel, TableState, Bet

from .domain import Player

class Engine:

    def __init__(
        self, 
        wheel: RouletteWheel,
        table: RouletteTable,
        catalog: BetCatalog,
        rules: Rules,
        limits: Limits
    ):  
        self.wheel = wheel
        self.table = table
        self.catalog = catalog
        self.rules = rules
        self.limits = limits

        self._state = TableState()

    def run(self, players: List[Player]):
        self.run_round(players)

    def run_round(self, players: List[Player]):
        self.initialize_round()

        for player in players:
            player_bets = player.place_bets(self.catalog, self.limits)
            self.accept_bets(player, player_bets)
        
        self.close_bets()
        self.spin_and_payout()

    def initialize_round(self) -> None:
        self._state = TableState()
        self.open_bets()

    def accept_bets(self, player: Player, player_bets: List[Bet]) -> None:
        self._state.bets[player] = player_bets

    def open_bets(self) -> None:
        self._state.bets_open = True

    def close_bets(self) -> None:
        self._state.bets_open = False

    def spin_and_payout(self) -> None:
        self._spin()
        self._evaluate_and_payout()

    def _spin(self) -> None:
        winning_numbers = self.wheel.spin()
        self._state.winning_numbers = winning_numbers

    def _evaluate_and_payout(self):
        winning_numbers = self._state.winning_numbers

        for player, bets in self._state.bets.items():
            for bet in bets:
                if bet.did_bet_hit(winning_numbers):
                    payout = bet.calculate_payout()
                    player.receive_payout(payout)