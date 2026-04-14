"""
Bootstrap module for initializing and running roulette simulations.
"""

from typing import List, Dict

from casino.roulette.domain.bet import BetCatalog
from casino.roulette.domain.table import RouletteTable

from .config import SimulationConfig
from .domain import RouletteWheel, Player, BetKind, BetDefinition, Bet, Rules, Limits, BetGroup, BetKind
from .engine import Engine
from .factories import PlayerFactory, BetCatalogFactory

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
        self._wheel: RouletteWheel | None = None
        self._players: List[Player] | None = None
        self._catalog: BetCatalog | None = None
        self._rules: Rules | None = None
        self._limits: Limits | None = None

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
                PlayerFactory.create(player_config)
                for player_config in self.config.players
            ]
        return self._players
    
    def build_wheel(self) -> RouletteWheel:
        """
        Build the wheel domain object from configuration.
        
        Returns:
            RouletteWheel value object with validation
        """
        if self._wheel is None:
            wheel = self.config.wheel
            self._wheel = RouletteWheel(
                num_balls=wheel.num_balls,
                num_zeros=wheel.num_zeros,
            )
        return self._wheel

    def build_catalog(self) -> BetCatalog:
        """
        Build the game bet catalog domain object from configuration.
        
        Returns:
            BetCatalog value object with validation
        """
        if self._catalog is None:
            self._catalog = BetCatalogFactory.create(self.config.bets)
        
        return self._catalog
    
    def build_rules(self) -> Rules:
        """
        Build the rules domain object from configuration.
        
        Returns:
            Rules value object with validation
        """
        if self._rules is None:
            rules = self.config.rules
            self._rules = Rules(
                la_partage=rules.la_partage,
                en_prison=rules.en_prison
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
            wheel=self.build_wheel(),
            table=RouletteTable(),
            # players=self.build_players(),
            catalog=self.build_catalog(),
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