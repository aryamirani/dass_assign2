import pytest
from moneypoly.property import Property, PropertyGroup
from moneypoly.player import Player

def test_property_initialization():
    group = PropertyGroup("Red", "red")
    prop = Property("Indiana", 23, 220, 18, group)
    assert prop.name == "Indiana"
    assert prop.position == 23
    assert prop.price == 220
    assert prop.base_rent == 18
    assert prop.mortgage_value == 110
    assert prop.owner is None
    assert prop.is_mortgaged is False
    assert prop.group == group
    assert prop in group.properties

def test_property_rent():
    group = PropertyGroup("Red", "red")
    prop1 = Property("Indiana", 23, 220, 18, group)
    prop2 = Property("Illinois", 24, 240, 20, group)
    
    player = Player("Alice")
    
    # Unowned
    assert prop1.get_rent() == 18
    
    # Single ownership
    prop1.owner = player
    assert prop1.get_rent() == 18
    
    # Full group ownership
    prop2.owner = player
    assert prop1.get_rent() == 36 # 18 * 2
    
    # Mortgaged
    prop1.mortgage()
    assert prop1.get_rent() == 0

def test_property_mortgage():
    prop = Property("Indiana", 23, 220, 18)
    
    # First mortgage
    payout = prop.mortgage()
    assert payout == 110
    assert prop.is_mortgaged is True
    
    # Second mortgage (returns 0)
    assert prop.mortgage() == 0

def test_property_unmortgage():
    prop = Property("Indiana", 23, 220, 18)
    
    # Not mortgaged
    assert prop.unmortgage() == 0
    
    # Mortgaged and unmortgaged
    prop.mortgage()
    cost = prop.unmortgage()
    assert cost == 121 # 110 * 1.1
    assert prop.is_mortgaged is False

def test_property_is_available():
    prop = Property("Indiana", 23, 220, 18)
    assert prop.is_available() is True
    
    prop.mortgage()
    assert prop.is_available() is False
    
    prop.unmortgage()
    prop.owner = Player("Alice")
    assert prop.is_available() is False

def test_property_group():
    group = PropertyGroup("Red", "red")
    prop1 = Property("Indiana", 23, 220, 18)
    prop2 = Property("Illinois", 24, 240, 20)
    
    group.add_property(prop1)
    group.add_property(prop2)
    assert group.size() == 2
    
    alice = Player("Alice")
    bob = Player("Bob")
    
    assert group.all_owned_by(alice) is False
    assert group.all_owned_by(None) is False
    
    prop1.owner = alice
    counts = group.get_owner_counts()
    assert counts[alice] == 1
    assert group.all_owned_by(alice) is False
    
    prop2.owner = alice
    assert group.all_owned_by(alice) is True

def test_property_reprs():
    group = PropertyGroup("Red", "red")
    prop = Property("Indiana", 23, 220, 18, group)
    assert repr(group) == "PropertyGroup('Red', 1 properties)"
    assert repr(prop) == "Property('Indiana', pos=23, owner='unowned')"
    prop.owner = Player("Alice")
    assert repr(prop) == "Property('Indiana', pos=23, owner='Alice')"
