import pytest
from casino.domain import Deck


@pytest.fixture
def single_deck():
    """Fixture for a single standard deck."""
    return Deck(number_of_decks=1, seed=42)


@pytest.fixture
def multi_deck():
    """Fixture for a 6-deck shoe."""
    return Deck(number_of_decks=6, seed=42)


def assert_valid_dealing_device_state(device) -> None:
    """Common invariant checks for dealing devices."""
    assert device.num_cards_dealt() + device.num_cards_remaining() == len(device)
    assert device.num_cards_dealt() >= 0
    assert device.num_cards_remaining() >= 0
    assert 0 <= device.num_cards_dealt() <= len(device)
    assert 0 <= device.num_cards_remaining() <= len(device)