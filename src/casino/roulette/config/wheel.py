from dataclasses import dataclass

@dataclass(frozen=True)
class WheelConfig:
    num_zeros: int
    num_balls: int = 1

    @classmethod
    def from_dict(cls, data: dict) -> "WheelConfig":
        """
        Parse and validate wheel configuration from raw dict.
        
        Args:
            data: Raw configuration dictionary
            
        Returns:
            Validated WheelConfig instance
        """
        return cls(
            num_zeros=data["num_zeros"],
            num_balls=data.get("num_balls", 1),
        )