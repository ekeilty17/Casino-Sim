from casino.blackjack.config.simulation import SimulationConfig
from casino.domain.deck import Deck
from casino.dealing import DealingDevice, Shoe, ContinuousShuffleMachine


class DealingDeviceFactory:
    """Factory for creating dealing device instances from configuration."""
    
    # Map device type names (case-insensitive) to device classes
    _DEVICE_MAP = {
        "shoe": Shoe,
        "csm": ContinuousShuffleMachine,
    }
    
    @classmethod
    def create_device(cls, config: SimulationConfig, deck: Deck) -> DealingDevice:
        """
        Create a dealing device instance from simulation configuration.
        
        Args:
            config: Simulation configuration containing dealing config
            deck: Deck instance to use with the device
            
        Returns:
            Instantiated dealing device
            
        Raises:
            ValueError: If device type is not recognized
        """
        device_type = config.dealing.device_type.lower().strip()
        
        if device_type not in cls._DEVICE_MAP:
            valid_devices = ", ".join(cls._DEVICE_MAP.keys())
            raise ValueError(
                f"Unknown dealing device: '{config.dealing.device_type}'. "
                f"Valid options: {valid_devices}"
            )
        
        device_class = cls._DEVICE_MAP[device_type]
        
        # Handle device-specific parameters
        if device_type == "shoe":
            return device_class(deck, penetration=config.dealing.penetration)
        else:  # csm
            return device_class(deck)