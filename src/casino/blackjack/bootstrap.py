"""
Bootstrap module for initializing and running blackjack simulations.

This module provides a clean separation between configuration parsing and
object construction, following the Dependency Injection and Factory patterns.
"""

from typing import List

from casino.domain.deck import Deck
from casino.dealing import DealingDevice
from casino.blackjack.config.simulation import SimulationConfig
from casino.blackjack.domain import Player, Rules, DoubleRule, SurrenderRule, Limits
from casino.blackjack.engine import Engine
from casino.blackjack.factories.dealing_device import DealingDeviceFactory
from casino.blackjack.factories.player import PlayerFactory


class SimulationBootstrapper:
    """
    Orchestrates the construction of all simulation components from configuration.
    
    This class follows the Builder pattern to construct complex object graphs
    in a controlled, testable manner. It ensures proper dependency injection
    and maintains separation of concerns between configuration and runtime objects.
    """
    
    def __init__(self, config: SimulationConfig):
        """
        Initialize the bootstrapper with simulation configuration.
        
        Args:
            config: Parsed simulation configuration
        """
        self.config = config
        self._deck: Deck | None = None
        self._dealing_device: DealingDevice | None = None
        self._players: List[Player] | None = None
        self._rules: Rules | None = None
        self._limits: Limits | None = None
    
    def build_deck(self) -> Deck:
        """
        Create and configure the deck for the simulation.
        
        Returns:
            Configured Deck instance
        """
        if self._deck is None:
            self._deck = Deck(
                number_of_decks=self.config.dealing.number_of_decks,
                seed=self.config.seed
            )
        return self._deck
    
    def build_dealing_device(self) -> DealingDevice:
        """
        Create and configure the dealing device.
        
        Returns:
            Configured DealingDevice instance
        """
        if self._dealing_device is None:
            deck = self.build_deck()
            self._dealing_device = DealingDeviceFactory.create_device(
                self.config, 
                deck
            )
        return self._dealing_device
    
    def build_players(self) -> List[Player]:
        """
        Create all player instances from configuration.
        
        Returns:
            List of configured Player instances
        """
        if self._players is None:
            # Reset player ID counter for consistent IDs across runs
            PlayerFactory.reset_counter()
            
            self._players = [
                PlayerFactory.create_player(player_config)
                for player_config in self.config.players
            ]
        return self._players
    
    def build_rules(self) -> Rules:
        """
        Build the game rules domain object from configuration.
        
        Returns:
            Rules value object with validated enums
        """
        if self._rules is None:
            rules = self.config.rules
            self._rules = Rules(
                dealer_hits_soft_17=rules.dealer_hits_soft_17,
                blackjack_payout=rules.blackjack_payout,
                double_after_split=rules.double_after_split,
                resplit_aces=rules.resplit_aces,
                hit_after_split_aces=rules.hit_after_split_aces,
                surrender=SurrenderRule[rules.surrender.upper()],
                dealer_peak=rules.dealer_peak,
                double=DoubleRule[rules.double.upper()],
                double_allowed_totals=frozenset(rules.double_allowed_totals),
                max_splits=rules.max_splits,
            )
        return self._rules
    
    def build_limits(self) -> Limits:
        """
        Build the table limits domain object from configuration.
        
        Returns:
            Limits value object with validation
        """
        if self._limits is None:
            limits = self.config.limits
            self._limits = Limits(
                min_bet=limits.min_bet,
                max_bet=limits.max_bet,
                max_table_bet=limits.max_table_bet,
            )
        return self._limits
    
    def build_engine(self) -> Engine:
        """
        Construct the complete simulation engine with all dependencies.
        
        This method orchestrates the construction of all components and
        injects them into the Engine.
        
        Returns:
            Fully configured Engine instance ready to run
        """
        return Engine(
            dealing_device=self.build_dealing_device(),
            players=self.build_players(),
            rules=self.build_rules(),
            limits=self.build_limits(),
        )
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "SimulationBootstrapper":
        """
        Create a bootstrapper from a raw configuration dictionary.
        
        This is a convenience method that handles the config parsing step.
        
        Args:
            config_dict: Raw configuration dictionary (e.g., from YAML)
            
        Returns:
            SimulationBootstrapper instance
        """
        config = SimulationConfig.from_dict(config_dict)
        print(config)
        return cls(config)


def run_simulation(config_dict: dict) -> None:
    """
    High-level function to run a simulation from raw configuration.
    
    This function provides a simple interface for running simulations,
    handling all the bootstrapping internally.
    
    Args:
        config_dict: Raw configuration dictionary (e.g., from YAML)
    """
    bootstrapper = SimulationBootstrapper.from_dict(config_dict)
    engine = bootstrapper.build_engine()
    engine.run()