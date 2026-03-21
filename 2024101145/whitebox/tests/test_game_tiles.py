import pytest
from unittest.mock import patch, MagicMock
from moneypoly.game import Game

@patch("builtins.print")
def test_move_to_go_to_jail(mock_print, monkeypatch):
    g = Game(["Alice"])
    p = g.players[0]
    p.position = 25 # Start somewhere
    g._move_and_resolve(p, 5) # Moves to 30 (Go To Jail)
    
    assert p.in_jail is True
    assert p.position == 10

@patch("builtins.print")
def test_move_to_income_tax(mock_print):
    g = Game(["Alice"])
    p = g.players[0]
    p.position = 0
    g._move_and_resolve(p, 4) # Income Tax
    
    assert p.balance == 1500 - 200 # INCOME_TAX_AMOUNT
    assert g.bank._total_collected == 200

@patch("builtins.print")
def test_move_to_luxury_tax(mock_print):
    g = Game(["Alice"])
    p = g.players[0]
    p.position = 35
    g._move_and_resolve(p, 3) # Luxury Tax (38)
    
    assert p.balance == 1500 - 75 # LUXURY_TAX_AMOUNT
    assert g.bank._total_collected == 75

@patch("builtins.print")
def test_move_to_free_parking(mock_print):
    g = Game(["Alice"])
    p = g.players[0]
    p.position = 15
    g._move_and_resolve(p, 5) # Free Parking (20)
    
    assert p.balance == 1500 # Unchanged

@patch("builtins.print")
def test_move_to_chance_and_community(mock_print, monkeypatch):
    g = Game(["Alice"])
    p = g.players[0]
    
    # Mock decks
    g.chance_deck = MagicMock()
    g.community_deck = MagicMock()
    
    g.chance_deck.draw.return_value = {"action": "collect", "value": 50, "description": "Bank pays you dividend"}
    g.community_deck.draw.return_value = {"action": "pay", "value": 50, "description": "Doctor's fees"}
    
    # Chance at 7
    p.position = 0
    g._move_and_resolve(p, 7)
    assert p.balance == 1550
    g.chance_deck.draw.assert_called_once()
    
    # Community Chest at 2
    p.position = 0
    g._move_and_resolve(p, 2)
    assert p.balance == 1500 # 1550 - 50
    g.community_deck.draw.assert_called_once()

@patch("builtins.print")
def test_move_to_railroad(mock_print):
    g = Game(["Alice", "Bob"])
    alice = g.players[0]
    bob = g.players[1]
    
    # Railroad at 5 (Reading Railroad)
    g.board.get_property_at(5).owner = bob
    
    alice.position = 0
    g._move_and_resolve(alice, 5)
    
    # Rent for railroad is 50 base * multiplier (1 because 1 owned... wait no, railroads have different logic?)
    # Wait, the code in game.py handles railroad via _handle_property_tile so rent depends on how many owned.
    # Base rent is hardcoded in initialization
    assert bob.balance == 1525
    assert alice.balance == 1475
