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
