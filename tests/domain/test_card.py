import pytest

from casino.domain.card import Rank, Suit, Card

def test_card_initialization():
    card = Card(rank=Rank.ACE, suit=Suit.SPADE)

    assert card.rank == Rank.ACE
    assert card.suit == Suit.SPADE


def test_card_invalid_pip_type():
    with pytest.raises(TypeError):
        Card(rank="A", suit=Suit.HEART)


def test_card_invalid_suit_type():
    with pytest.raises(TypeError):
        Card(rank=Rank.ACE, suit="HEART")


def test_card_is_immutable():
    card = Card(rank=Rank.ACE, suit=Suit.HEART)

    with pytest.raises(Exception):
        card.rank = Rank.KING


def test_card_equality():
    c1 = Card(Rank.ACE, Suit.SPADE)
    c2 = Card(Rank.ACE, Suit.SPADE)
    c3 = Card(Rank.KING, Suit.SPADE)

    assert c1 == c2
    assert c1 != c3


def test_card_hashing():
    c1 = Card(Rank.ACE, Suit.SPADE)
    c2 = Card(Rank.ACE, Suit.SPADE)

    assert hash(c1) == hash(c2)

    card_set = {c1, c2}
    assert len(card_set) == 1


def test_card_str():
    card = Card(Rank.ACE, Suit.SPADE)
    assert str(card) == "A♠"


def test_card_repr():
    card = Card(Rank.ACE, Suit.SPADE)
    r = repr(card)

    assert "Card" in r
    assert "ACE" in r
    assert "SPADE" in r


def test_pip_ordering():
    assert Rank.ACE < Rank.TWO
    assert Rank.TEN < Rank.JACK
    assert Rank.QUEEN < Rank.KING


def test_suit_symbols():
    assert str(Suit.HEART) == "♥"
    assert str(Suit.CLUB) == "♣"
    assert str(Suit.DIAMOND) == "♦"
    assert str(Suit.SPADE) == "♠"


def test_cards_are_distinct_by_pip_and_suit():
    c1 = Card(Rank.ACE, Suit.SPADE)
    c2 = Card(Rank.ACE, Suit.HEART)

    assert c1 != c2


@pytest.mark.parametrize(
    "pip,suit,expected",
    [
        (Rank.ACE, Suit.SPADE, "A♠"),
        (Rank.KING, Suit.HEART, "K♥"),
        (Rank.TEN, Suit.DIAMOND, "10♦"),
        (Rank.TWO, Suit.CLUB, "2♣"),
    ],
)
def test_card_str_parametrized(pip, suit, expected):
    card = Card(pip, suit)
    assert str(card) == expected