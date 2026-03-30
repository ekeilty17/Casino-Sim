import os
import argparse
import yaml

from casino.blackjack.bootstrap import SimulationBootstrapper


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run BlackJack simulation.")
    parser.add_argument(
        "config_path",
        help="Path to the YAML simulation configuration file"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging."
    )
    return parser.parse_args()


def load_config(config_path: str) -> dict:
    """
    Load and parse the YAML configuration file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Parsed configuration dictionary
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    """Main entry point for the blackjack simulation CLI."""
    args = parse_args()
    
    # Load configuration from YAML file
    config_dict = load_config(args.config_path)
    
    # Bootstrap and run the simulation
    bootstrapper = SimulationBootstrapper.from_dict(config_dict)
    engine = bootstrapper.build_engine()
    engine.run()


if __name__ == "__main__":
    main()