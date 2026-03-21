# Assignment 2: Software Testing
**Roll Number:** 2024101145

## Project Structure
- `whitebox/`: White Box Testing of the Money-Poly game.
  - `code/`: Corrected Money-Poly source code (Pylint 10/10).
  - `tests/`: Pytest suite achieving branch coverage and verification of 11 logic bugs.
  - `report.md`: Documentation of Pylint iterations and bug fixes.
  - `diagrams/`: Control Flow Graph (Hand-drawn).
- `integration/`: Integration Testing of the StreetRace Manager.
  - `code/`: Modular implementation of 8 integrated modules.
  - `tests/`: Pytest suite verifying cross-module business rules.
  - `report.md`: Architecture overview and test design.
  - `diagrams/`: Call Graph (Hand-drawn).
- `blackbox/`: Black Box testing of the QuickCart API.
  - `tests/`: Pytest suite using `requests` to validate documentation rules.
  - `report.md`: Test design and detailed bug report of 4 server-side errors.

## Execution Instructions

### Prerequisites
- Python 3.9+
- Docker (for QuickCart API)

### Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install pytest pytest-cov requests pylint
   ```

### Running Tests
- **White Box**: `PYTHONPATH=2024101145/whitebox/code pytest 2024101145/whitebox/tests/`
- **Integration**: `PYTHONPATH=2024101145/integration/code pytest 2024101145/integration/tests/`
- **Black Box**: (Ensure the QuickCart docker server is running on localhost:8080) `pytest 2024101145/blackbox/tests/`

## Git Repository
[https://github.com/aryamirani/dass_assign2](https://github.com/aryamirani/dass_assign2)
