# White Box Testing Report

## 1.2 Code Quality Analysis
The `moneypoly` codebase was analyzed using `pylint`. Initially, the codebase scored around 9.08/10, exhibiting several issues such as missing docstrings, lines being too long, unexpected variable definitions, design warnings (too many arguments/attributes/branches), and formatting inconsistencies.

We iteratively fixed the code as per the warnings and suggestions, and documented each iteration as a commit.

### Iterations Documented
- **Iteration 1**: Added missing module and function docstrings to `main.py`.
- **Iteration 2**: Added module docstring to `board.py` and fixed the singleton boolean comparison (`is_mortgaged == True`).
- **Iteration 3**: Added module docstring to `config.py`.
- **Iteration 4**: Added docstrings to `property.py` and resolved an unnecessary `else` after a `return` block.
- **Iteration 5**: Added missing module docstring to `ui.py` and changed a bare `except:` to `except ValueError:`.
- **Iteration 6**: Fixed multiple issues in `game.py` including `superfluous-parens`, missing `module-docstring`, `f-string-without-interpolation`, `no-else-break`, and removed unused imports.
- **Iteration 7**: Added missing module docstring to `cards.py` and disabled the `line-too-long` warning to preserve the structural readability of the card dictionaries.
- **Iteration 8**: Added missing module docstring to `dice.py`, resolved `attribute-defined-outside-init` by moving `self.doubles_streak = 0` to `__init__`, and removed an unused import.
- **Iteration 9**: Added module and class docstrings to `bank.py` and removed an unused `import math`.
- **Iteration 10**: Added missing module docstring to `player.py`, fixed a duplicate self-assignment, and removed an unused import.
- **Iteration 11**: Final compilation round to resolve missing EOF newlines in `game.py` and `player.py`, trailing whitespace in `property.py`, and correctly placing pylint disable rules out of docstrings for design warnings (`too-many-instance-attributes`, `too-many-branches`, `too-many-arguments`).

**Final Result**: The `pylint` score achieved a perfect **10.00/10**.

## 1.3 White Box Test Cases
We utilized `pytest` combined with `unittest.mock` and `monkeypatch` to test all modules: `bank.py`, `board.py`, `cards.py`, `config.py`, `dice.py`, `player.py`, `property.py`, and the exhaustive integration interactions in `game.py`.
The intent was to achieve full branch coverage (every decision path), manipulate key variable states (like forcing doubles, testing jail fines, setting up bankruptcies), and testing edge cases (such as negative deposits, 0 bids in auctions, and empty property lists).
Through rigorous testing matching over 87% of the possible branches according to `pytest-cov`, we uncovered **11 distinct logical errors** in the original Money-Poly source code. Each test case was designed to simulate these exact scenarios to predictably trigger the bugs before implementing their fixes.

### Errors and Logical Issues Fixed

1. **Error 1: Bank Collect and Loan Deduction**  
   - *Test specific:* Added a test depositing `-100` to the bank, and an emergency loan test. The bug was that `bank.collect` added negative amounts instead of purposefully ignoring them as required, and `bank.give_loan` credited the player but never formally deducted the funds from the bank reserves!
2. **Error 2: Player Move and Property Assignment**  
   - *Test specific:* Simulated a player moving past the absolute position `0` from the end of the board, and an organic property acquisition. The bug was `player.move` didn't correctly award `GO_SALARY` when wrapping the board array boundary, and `add_property` didn't link the `.owner` relation back to the instantiating player.
3. **Error 3: Group Ownership Evaluation**  
   - *Test specific:* Added multiple properties to a property group and formally assigned one to `Alice`. The bug was that `PropertyGroup.all_owned_by()` incorrectly utilized `any()` instead of `all()`, resulting in single-owned property sets artificially triggering the `FULL_GROUP_MULTIPLIER` penalty!
4. **Error 4: Missing Rent Transfers**  
   - *Test specific:* Sent a player to another player's unmortgaged property spot. The bug was that `game.pay_rent` simply deducted money from `player.balance` but effectively evaporated it instead of securely adding it to the matching `prop.owner.balance`.
5. **Error 5: Backwards Mortgage Payouts**  
   - *Test specific:* Instructed a player to intentionally mortgage their property for cash via the menu simulation mock. The bug was that `game.mortgage_property` called `self.bank.collect(-payout)` which processed as silent failure instead of a mathematically correct `bank.pay_out()` to represent cash exiting the bank reserves.
6. **Error 6: Trade Unidirectional Cash Exchange**  
   - *Test specific:* Initiated an interactive trade sequence between distinct players Alice and Bob. The bug was that `game.trade` deducted the cash from the buyer dynamically to purchase the property, but didn't successfully credit the `cash_amount` sum to the corresponding seller!
7. **Error 7: Jail Turn Neglect**  
   - *Test specific:* Triggered 3 consecutive turns in jail where the player actively refused to pay the fine. The bug was that the original design implementation only incrementally logged `player.jail_turns` but completely forgot to implement the actual ability to probabilistically roll the dice to try for doubles to break out.
8. **Error 8: Backwards Winner Selection**  
   - *Test specific:* Executed `find_winner` manually over two dummy players with distinct balances. The bug was that the list sorting mechanism explicitly used `min()` instead of `max()`, unintentionally guaranteeing the poorest, least successful player was historically declared the winner!
9. **Error 9: Neglected Jail Fines**  
   - *Test specific:* The player accepted the boolean confirm prompt to pay their way out of jail instead of using an itemized card or actively rolling. The bug was that the `JAIL_FINE` was fully logged to the bank properties, but was never actually deducted physically from the player's balance sheet.
10. **Error 10: Missing Board Railroads**  
    - *Test specific:* Deployed chance cards and raw absolute location integer jumps to actively force the `prop is not None` overarching branch in `game.py`. The fundamental bug was that none of the four traditional Monopoly Railroads were actually functionally initialized in `board.py`, rendering the entire rail network completely non-callable!
11. **Error 11: Ignore Railroad Landings**  
    - *Test specific:* Enforced drawing a "move to explicitly targeted position 15 (Reading/Pennsylvania Railroad)" sequence chance card during a formal turn. The bug was that `apply_card()` rigorously verified whether the physical landing tile was exclusively `"property"`, completely ignoring tiles inherently identified separately as `"railroad"`.
