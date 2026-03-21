import pytest
from moneypoly.board import Board
from moneypoly.player import Player

def test_board_initialization():
    b = Board()
    assert len(b.groups) == 9
    assert len(b.properties) == 26
    assert repr(b) == "Board(26 properties, 0 owned)"

def test_board_get_property_at():
    b = Board()
    
    prop = b.get_property_at(1)
    assert prop is not None
    assert prop.name == "Mediterranean Avenue"
    
    assert b.get_property_at(0) is None # GO space
    assert b.get_property_at(99) is None # Out of bounds

def test_board_get_tile_type():
    b = Board()
    
    assert b.get_tile_type(0) == "go"
    assert b.get_tile_type(10) == "jail"
    assert b.get_tile_type(1) == "property"
    assert b.get_tile_type(2) == "community_chest"
    assert b.get_tile_type(5) == "railroad"
    assert b.get_tile_type(38) == "luxury_tax"
    assert b.get_tile_type(12) == "blank" # e.g. Electric Company doesn't exist in properties list here

def test_board_is_purchasable():
    b = Board()
    
    assert b.is_purchasable(1) is True # unowned, not mortgaged
    assert b.is_purchasable(0) is False # GO
    
    prop = b.get_property_at(1)
    prop.mortgage()
    assert b.is_purchasable(1) is False
    
    prop.unmortgage()
    prop.owner = Player("Alice")
    assert b.is_purchasable(1) is False

def test_board_is_special_tile():
    b = Board()
    
    assert b.is_special_tile(0) is True
    assert b.is_special_tile(10) is True
    assert b.is_special_tile(1) is False

def test_board_properties_owned_and_unowned():
    b = Board()
    alice = Player("Alice")
    
    assert len(b.unowned_properties()) == 26
    assert len(b.properties_owned_by(alice)) == 0
    
    prop1 = b.get_property_at(1)
    prop1.owner = alice
    
    assert len(b.unowned_properties()) == 25
    assert len(b.properties_owned_by(alice)) == 1
    assert b.properties_owned_by(alice)[0].name == "Mediterranean Avenue"
