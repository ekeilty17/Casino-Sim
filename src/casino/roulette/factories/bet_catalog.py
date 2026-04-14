from ..config import BetsConfig
from ..domain import RouletteNumber, BetCatalog, BetDefinition, BetKind, BetGroup


class BetCatalogFactory:

    @classmethod
    def create(cls, config: BetsConfig) -> BetCatalog:
        catalog = {}
        for name, definition_config in config.definitions.items():

            numbers = None
            if definition_config.numbers is not None:
                numbers = tuple(
                    RouletteNumber.from_label(number_str) 
                    for number_str in definition_config.numbers
                )
            
            catalog[name] = BetDefinition(
                name=definition_config.name,
                group=BetGroup(definition_config.group),
                kind=BetKind(definition_config.kind),
                odds=definition_config.odds,
                numbers=numbers
            )
        
        return BetCatalog(catalog)