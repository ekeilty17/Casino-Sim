import pytest

from casino.core.card import Card, Pip, Suit


def test_card_initialization():
    card = Card(pip=Pip.ACE, suit=Suit.SPADE)

    assert card.pip == Pip.ACE
    assert card.suit == Suit.SPADE


def test_card_invalid_pip_type():
    with pytest.raises(TypeError):
        Card(pip="A", suit=Suit.HEART)


def test_card_invalid_suit_type():
    with pytest.raises(TypeError):
        Card(pip=Pip.ACE, suit="HEART")


def test_card_is_immutable():
    card = Card(pip=Pip.ACE, suit=Suit.HEART)

    with pytest.raises(Exception):
        card.pip = Pip.KING


def test_card_equality():
    c1 = Card(Pip.ACE, Suit.SPADE)
    c2 = Card(Pip.ACE, Suit.SPADE)
    c3 = Card(Pip.KING, Suit.SPADE)

    assert c1 == c2
    assert c1 != c3


def test_card_hashing():
    c1 = Card(Pip.ACE, Suit.SPADE)
    c2 = Card(Pip.ACE, Suit.SPADE)

    assert hash(c1) == hash(c2)

    card_set = {c1, c2}
    assert len(card_set) == 1


def test_card_str():
    card = Card(Pip.ACE, Suit.SPADE)
    assert str(card) == "A♠"


def test_card_repr():
    card = Card(Pip.ACE, Suit.SPADE)
    r = repr(card)

    assert "Card" in r
    assert "ACE" in r
    assert "SPADE" in r


def test_pip_ordering():
    assert Pip.ACE < Pip.TWO
    assert Pip.TEN < Pip.JACK
    assert Pip.QUEEN < Pip.KING


def test_suit_symbols():
    assert str(Suit.HEART) == "♥"
    assert str(Suit.CLUB) == "♣"
    assert str(Suit.DIAMOND) == "♦"
    assert str(Suit.SPADE) == "♠"


def test_cards_are_distinct_by_pip_and_suit():
    c1 = Card(Pip.ACE, Suit.SPADE)
    c2 = Card(Pip.ACE, Suit.HEART)

    assert c1 != c2


@pytest.mark.parametrize(
    "pip,suit,expected",
    [
        (Pip.ACE, Suit.SPADE, "A♠"),
        (Pip.KING, Suit.HEART, "K♥"),
        (Pip.TEN, Suit.DIAMOND, "10♦"),
        (Pip.TWO, Suit.CLUB, "2♣"),
    ],
)
def test_card_str_parametrized(pip, suit, expected):
    card = Card(pip, suit)
    assert str(card) == expected