from dataclasses import dataclass

@dataclass(frozen=True)
class RulesConfig:
    la_partage: bool = False
    en_prison: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "RulesConfig":
        """
        Parse and validate rules configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary
            
        Returns:
            Validated RulesConfig instance
        """
        return cls(
            la_partage=data.get("la_partage", False),
            en_prison=data.get("en_prison", False),
        )