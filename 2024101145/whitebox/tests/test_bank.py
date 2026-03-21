import pytest
from moneypoly.bank import Bank
from moneypoly.player import Player

def test_bank_initialization():
    bank = Bank()
    assert bank.get_balance() == 20580
    assert bank.total_loans_issued() == 0
    assert bank.loan_count() == 0
    assert bank._total_collected == 0

def test_bank_collect():
    bank = Bank()
    bank.collect(500)
    assert bank.get_balance() == 21080
    assert bank._total_collected == 500
    
    # Test negative collection (silently ignored as per docstring... wait, the docstring says it is, but the code doesn't actually ignore it. Let's see if we catch a bug here or test the actual behavior.)
    # Actually, the docstring says: "Negative amounts are silently ignored.", but the code is `self._funds += amount`.
    # Let's write the test according to the docstring to catch the bug!
    bank.collect(-100)
    # The expected behavior based on the docstring is that balance remains 21080. But the bug will lower it.
    # We will test for the EXPECTED behavior (White Box Testing) and see it fail.
    # Actually wait. White box testing means we test the code structure. The code does not have an `if amount < 0` check.
    # So a branch doesn't exist. Let's just test that it DOES reduce the amount (to document the bug) or test what the docstring says.
    # Usually we test against requirements. Let's assert based on the docstring so it fails.
    assert bank.get_balance() == 21080

def test_bank_pay_out():
    bank = Bank()
    
    # Normal payout
    paid = bank.pay_out(580)
    assert paid == 580
    assert bank.get_balance() == 20000
    
    # Negative/Zero payout (returns 0)
    assert bank.pay_out(0) == 0
    assert bank.pay_out(-50) == 0
    assert bank.get_balance() == 20000
    
    # Insufficient funds raises ValueError
    with pytest.raises(ValueError, match="Bank cannot pay"):
        bank.pay_out(30000)

def test_bank_give_loan():
    bank = Bank()
    player = Player("Alice")
    
    # Normal loan
    bank.give_loan(player, 500)
    assert player.balance == 2000 # 1500 start + 500
    assert bank.loan_count() == 1
    assert bank.total_loans_issued() == 500
    # BUG: bank's _funds are NOT reduced in the give_loan function!
    # Let's test for the expected requirement according to the docstring.
    assert bank.get_balance() == 20080

    # Zero/negative loan
    bank.give_loan(player, 0)
    bank.give_loan(player, -100)
    assert bank.loan_count() == 1

def test_bank_summary(capsys):
    bank = Bank()
    bank.summary()
    captured = capsys.readouterr()
    assert "Bank reserves" in captured.out
    
def test_bank_repr():
    bank = Bank()
    assert repr(bank) == "Bank(funds=20580)"
