import pytest
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup

def test_player_initialization():
    p = Player("Alice")
    assert p.name == "Alice"
    assert p.balance == 1500
    assert p.position == 0
    assert p.in_jail is False
    assert p.jail_turns == 0
    assert p.get_out_of_jail_cards == 0
    assert len(p.properties) == 0

def test_player_money():
    p = Player("Alice")
    
    p.add_money(500)
    assert p.balance == 2000
    
    # Adding negative amount raises ValueError
    with pytest.raises(ValueError):
        p.add_money(-100)
    assert p.balance == 2000
    
    p.deduct_money(1000)
    assert p.balance == 1000
    
    # Subtracting negative raises ValueError
    with pytest.raises(ValueError):
        p.deduct_money(-50)
    assert p.balance == 1000

def test_player_move(capsys):
    p = Player("Alice")
    
    # Simple move
    pos = p.move(5)
    assert pos == 5
    assert p.position == 5
    
    # Move past GO collects $200 salary
    # BOARD_SIZE is 40. Start at 38, move 5 -> 43 % 40 = 3
    p.position = 38
    pos = p.move(5)
    assert pos == 3
    assert p.balance == 1700 # 1500 (start) + 200 (GO salary)
    
    # Move exactly onto GO (40)
    p.position = 35
    pos = p.move(5)
    assert pos == 0
    assert p.balance == 1900 # 1700 + 200

def test_player_go_to_jail():
    p = Player("Alice")
    
    p.go_to_jail()
    assert p.in_jail is True
    assert p.position == 10 # JAIL_POSITION
    assert p.jail_turns == 0

def test_player_jail_turns():
    p = Player("Alice")
    p.go_to_jail()
    
    p.jail_turns += 1
    assert p.jail_turns == 1
    
    p.jail_turns += 1
    assert p.jail_turns == 2
    
    p.jail_turns += 1
    assert p.jail_turns == 3

def test_player_get_out_of_jail():
    p = Player("Alice")
    p.go_to_jail()
    p.jail_turns = 2
    
    p.in_jail = False
    p.jail_turns = 0
    assert p.in_jail is False
    assert p.jail_turns == 0
    # Position remains JAIL_POSITION, must roll to move out on next turn

def test_player_jail_free_cards():
    p = Player("Alice")
    
    assert p.get_out_of_jail_cards == 0
    p.get_out_of_jail_cards += 1
    assert p.get_out_of_jail_cards == 1
    
    p.get_out_of_jail_cards -= 1
    assert p.get_out_of_jail_cards == 0

    pass

def test_player_add_property():
    p = Player("Alice")
    group = PropertyGroup("Red", "red")
    prop = Property("Indiana", 23, 220, 18, group)
    
    p.add_property(prop)
    assert len(p.properties) == 1
    assert prop.owner == p
    
    # Duplicate add
    p.add_property(prop)
    assert len(p.properties) == 1 # Code checks `if property not in self.properties`

def test_player_remove_property():
    p = Player("Alice")
    group = PropertyGroup("Red", "red")
    prop = Property("Indiana", 23, 220, 18, group)
    
    p.add_property(prop)
    p.remove_property(prop)
    assert len(p.properties) == 0
    assert prop.owner is None
    
    # Remove when not owned
    p.remove_property(prop) # Shouldn't raise error

def test_player_is_bankrupt():
    p = Player("Alice")
    
    assert p.is_bankrupt() is False
    
    p.deduct_money(1500)
    assert p.is_bankrupt() is True # balance is 0 or less
    
    p.deduct_money(100)
    assert p.is_bankrupt() is True

def test_player_repr():
    p = Player("Alice")
    assert repr(p) == "Player('Alice', balance=1500, pos=0)"
