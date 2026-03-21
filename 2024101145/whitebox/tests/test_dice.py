import pytest
from moneypoly.dice import Dice

def test_dice_initialization():
    d = Dice()
    assert d.die1 == 0
    assert d.die2 == 0
    assert d.doubles_streak == 0

def test_dice_roll(monkeypatch):
    d = Dice()
    
    # Mock random to return fixed values to test branches
    # Test non-doubles
    monkeypatch.setattr("random.randint", lambda a, b: 3 if getattr(test_dice_roll, "call_count", 0) == 0 else 4)
    test_dice_roll.call_count = 0
    def mock_randint(a, b):
        test_dice_roll.call_count += 1
        return 3 if test_dice_roll.call_count == 1 else 4
    monkeypatch.setattr("random.randint", mock_randint)
    
    total = d.roll()
    assert total == 7
    assert d.is_doubles() is False
    assert d.doubles_streak == 0
    assert d.describe() == "3 + 4 = 7"
    
    # Test doubles
    test_dice_roll.call_count = 0
    def mock_randint_doubles(a, b):
        return 5
    monkeypatch.setattr("random.randint", mock_randint_doubles)
    
    total = d.roll()
    assert total == 10
    assert d.is_doubles() is True
    assert d.doubles_streak == 1
    assert d.describe() == "5 + 5 = 10 (DOUBLES)"
    
    # Roll doubles again
    d.roll()
    assert d.doubles_streak == 2

def test_dice_repr():
    d = Dice()
    assert repr(d) == "Dice(die1=0, die2=0, streak=0)"
