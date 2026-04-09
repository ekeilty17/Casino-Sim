from typing import Dict, List, Any, Set

from casino.blackjack.domain import Action

from .base import DecisionStrategy, DecisionContext

class HumanInputDecisionStrategy(DecisionStrategy):

    _ACTION_INPUT: List[Dict[str, Any]] = [
        {"symbol": "H", "name": "Hit", "action": Action.HIT},
        {"symbol": "S", "name": "Stand", "action": Action.STAND},
        {"symbol": "R", "name": "Surrender", "action": Action.SURRENDER},
        {"symbol": "D", "name": "Double", "action": Action.DOUBLE},
        {"symbol": "P", "name": "Split", "action": Action.SPLIT},
    ]

    def decide(self, context: DecisionContext) -> Action:
        
        action: Action | None = None
        while True:
            HumanInputDecisionStrategy._display_context(context)

            user_options_string = HumanInputDecisionStrategy._construct_user_options(context.actions)
            user_options_string += "\n\nSelection: "
            user_selection = input(user_options_string)
            action = HumanInputDecisionStrategy._parse_selection(user_selection)
            
            if action in context.actions:
                return action
            
            print(f"'{user_selection}' is not a valid option. Please try again.\n")

    @staticmethod
    def _display_context(context: DecisionContext) -> None:
        print("Dealer Upcard:", str(context.dealer_upcard))
        print("Player Hand  :", str(context.hand.cards))
        print()

    @staticmethod
    def _construct_user_options(allowed_actions: Set[Action]) -> str:
        output = "Choose from one of the following options:"

        allowed_action_objs = [obj for obj in HumanInputDecisionStrategy._ACTION_INPUT if obj["action"] in allowed_actions]
        for obj in allowed_action_objs:
            output += f"\n\t({obj['symbol']}) {obj['name']}"
        
        return output

    @staticmethod
    def _parse_selection(user_selection: str) -> Action | None:
        for obj in HumanInputDecisionStrategy._ACTION_INPUT:
            if user_selection == obj["symbol"]:
                return obj["action"]