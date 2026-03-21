import pytest
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.bank import Bank

def test_player_creation():
    p = Player("Alice")
    assert p.name == "Alice"
    assert p.balance == 1500
    assert p.position == 0
