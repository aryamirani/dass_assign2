import pytest
from unittest.mock import patch, MagicMock
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.board import Board
from moneypoly.dice import Dice
from moneypoly.cards import CHANCE_CARDS
import moneypoly.ui as ui
import builtins

def test_game_initialization():
    g = Game(["Alice", "Bob"])
    assert len(g.players) == 2
    assert g.players[0].name == "Alice"
    assert g.players[1].name == "Bob"
    assert isinstance(g.board, Board)
    assert isinstance(g.dice, Dice)
    assert g.current_index == 0
    assert g.turn_number == 0
    assert g.running is True
    assert g.current_player().name == "Alice"

def test_advance_turn():
    g = Game(["Alice", "Bob"])
    g.advance_turn()
    assert g.current_index == 1
    assert g.turn_number == 1
    g.advance_turn()
    assert g.current_index == 0
    assert g.turn_number == 2

@patch("builtins.print")
def test_play_turn_normal(mock_print, monkeypatch):
    g = Game(["Alice", "Bob"])
    monkeypatch.setattr(g.dice, "roll", lambda: 5)
    monkeypatch.setattr(g.dice, "is_doubles", lambda: False)
    
    # We mock _handle_property_tile so it doesn't wait for input
    g._handle_property_tile = MagicMock()
    g.play_turn()
    
    assert g.players[0].position == 5
    assert g.current_index == 1 # Advanced to next player

@patch("builtins.print")
def test_play_turn_doubles(mock_print, monkeypatch):
    g = Game(["Alice", "Bob"])
    
    # Mock roll returns 5, is_doubles returns True
    monkeypatch.setattr(g.dice, "roll", lambda: 5)
    monkeypatch.setattr(g.dice, "is_doubles", lambda: True)
    g.dice.doubles_streak = 1
    g._handle_property_tile = MagicMock()
    
    g.play_turn()
    
    assert g.players[0].position == 5
    assert g.current_index == 0 # Earned extra turn
    
    # 3 doubles sends to jail
    g.dice.doubles_streak = 3
    g.play_turn()
    assert g.players[0].in_jail is True
    assert g.players[0].position == 10
    assert g.current_index == 1 # Turn ends

@patch("moneypoly.ui.safe_int_input")
@patch("builtins.input")
def test_property_interaction(mock_input, mock_safe_int_input, monkeypatch):
    g = Game(["Alice", "Bob"])
    player = g.players[0]
    prop = g.board.get_property_at(1) # Mediterranean Ave ($60)
    
    # Buy choice
    mock_input.return_value = "b"
    g._handle_property_tile(player, prop)
    assert prop.owner == player
    assert player.balance == 1500 - 60
    
    # Land on own property
    g._handle_property_tile(player, prop)
    assert player.balance == 1440
    
    # Bob lands on Alice's property -> Pays rent (base rent is $2)
    bob = g.players[1]
    g._handle_property_tile(bob, prop)
    assert bob.balance == 1498
    assert player.balance == 1442
    
    # Skip choice
    prop2 = g.board.get_property_at(3)
    mock_input.return_value = "s"
    g._handle_property_tile(player, prop2)
    assert prop2.owner is None
    
    # Auction choice
    mock_input.return_value = "a"
    g.auction_property = MagicMock()
    g._handle_property_tile(player, prop2)
    g.auction_property.assert_called_with(prop2)

@patch("moneypoly.ui.safe_int_input")
def test_auction_logic(mock_safe_int_input):
    g = Game(["Alice", "Bob"])
    prop = g.board.get_property_at(1)
    
    mock_safe_int_input.side_effect = [50, 0]
    g.auction_property(prop)
    
    assert prop.owner == g.players[0]
    assert g.players[0].balance == 1450

@patch("moneypoly.ui.safe_int_input")
def test_auction_no_bids(mock_safe_int_input):
    g = Game(["Alice", "Bob"])
    prop = g.board.get_property_at(1)
    mock_safe_int_input.side_effect = [0, 0]
    g.auction_property(prop)
    assert prop.owner is None

def test_mortgage_and_unmortgage():
    g = Game(["Alice", "Bob"])
    player = g.players[0]
    prop = g.board.get_property_at(1) # $60
    
    prop.owner = player
    player.add_property(prop)
    
    # Mortgage
    assert g.mortgage_property(player, prop) is True
    assert prop.is_mortgaged is True
    assert player.balance == 1500 + 30 # Mortgage value $30

def test_trade_logic():
    g = Game(["Alice", "Bob"])
    alice = g.players[0]
    bob = g.players[1]
    prop = g.board.get_property_at(1)
    
    prop.owner = alice
    alice.add_property(prop)
    
    assert g.trade(alice, bob, prop, 100) is True
    assert prop.owner == bob
    assert bob.balance == 1400
    assert alice.balance == 1600

@patch("moneypoly.ui.confirm")
def test_jail_turn_pay_fine(mock_confirm, monkeypatch):
    g = Game(["Alice", "Bob"])
    alice = g.players[0]
    alice.go_to_jail()
    
    mock_confirm.return_value = True
    monkeypatch.setattr(g.dice, "roll", lambda: 5)
    g._handle_property_tile = MagicMock()
    
    g._handle_jail_turn(alice)
    
    assert alice.in_jail is False
    assert alice.balance == 1500 - 50
    assert alice.position == 15

@patch("moneypoly.ui.confirm")
def test_jail_turn_roll_doubles(mock_confirm, monkeypatch):
    g = Game(["Alice", "Bob"])
    alice = g.players[0]
    alice.go_to_jail()
    
    mock_confirm.return_value = False
    monkeypatch.setattr(g.dice, "roll", lambda: 8)
    monkeypatch.setattr(g.dice, "is_doubles", lambda: True)
    g._handle_property_tile = MagicMock()
    
    g._handle_jail_turn(alice)
    
    assert alice.in_jail is False
    assert alice.jail_turns == 0
    assert alice.position == 18

def test_bankruptcy():
    g = Game(["Alice", "Bob"])
    alice = g.players[0]
    
    alice.deduct_money(1500) # Bankrupt
    g._check_bankruptcy(alice)
    
    assert alice.is_eliminated is True
    assert alice not in g.players

def test_winner():
    g = Game(["Alice", "Bob"])
    # BUG IDENTIFIED IN WINNER LOGIC `min(players)` instead of `max(players)`!!!
    # Let's see if our logic proves it:
    g.players[0].add_money(100) # Alice has 1600
    g.players[1].deduct_money(100) # Bob has 1400
    assert g.find_winner().name == "Alice"
