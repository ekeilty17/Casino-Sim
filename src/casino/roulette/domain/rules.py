from dataclasses import dataclass

@dataclass(frozen=True)
class Rules:
    la_partage: bool
    en_prison: bool