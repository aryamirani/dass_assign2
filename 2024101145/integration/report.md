# Integration Testing Report

## StreetRace Manager Architecture
The StreetRace Manager system is built using eight modular components that interact closely to manage crews, assets, and races:
1. **Registration**: Registers new crew members and stores their roles.
2. **Crew Management**: Manages roles and records skill levels for crew members (Integrates with Registration).
3. **Inventory**: Tracks cars, spare parts, tools, and cash balance.
4. **Race Management**: Creates races and enforces driver/car business rules for entering (Integrates with Crew Management and Inventory).
5. **Results**: Records race outcomes, updates the leaderboard, handles prize money, and applies randomized damage to cars (Integrates with Race Management and Inventory).
6. **Mission Planning**: Assigns special missions verifying required roles and minimum car conditions (Integrates with Crew Management and Inventory).

### Custom Modules
7. **Garage**: Allows a registered "mechanic" to repair damaged cars back to 100% condition using spare parts and tools from the inventory (Integrates with Crew Management and Inventory).
8. **Rivalry**: Tracks heat and rivalry levels with opposing crews. High rivalry (>80) leads to enemy interference, automatically increasing the difficulty of an upcoming race (Integrates with Race Management).

## 2.2 Integration Test Design
The following Pytest scenarios were implemented in `tests/test_integration.py` to validate module interactions according to business rules:

### Scenario 1: Registering a Driver and Entering a Race
- **Modules Involved**: Registration, Crew Management, Inventory, Race Management
- **Description**: Verifies the "happy path" where a valid `driver` is registered, assigned skills, a car is logged in inventory, a race is created, and the driver successfully enters it.
- **Expected/Actual Result**: The driver is successfully added to the race's participant list because they perfectly satisfy the business role constraint and the car condition constraint. No logical errors found.

### Scenario 2: Attempting to Enter Race Without Registered Driver
- **Modules Involved**: Crew Management, Inventory, Race Management
- **Description**: Verifies the business rule that un-registered individuals, or members without the explicitly required "driver" role, are blocked from entering.
- **Expected/Actual Result**: The system actively raises a `ValueError` indicating the individual is not a registered driver, blocking entry.

### Scenario 3: Completing a Race and Verifying Result Flow
- **Modules Involved**: Race Management, Inventory, Results
- **Description**: Records a race winner, verifying that prize money (calculated via difficulty multipliers) is dynamically deposited into the Inventory cash balance, the leaderboard updates, and participated cars take randomized damage.
- **Expected/Actual Result**: Cash increases appropriately ($15k), the leaderboard logs +10 points, and the used car's condition drops below 100%. No logical errors found.

### Scenario 4: Assigning a Mission Role Validation
- **Modules Involved**: Registration, Crew Management, Mission Planning
- **Description**: Attempts to start a mission that requires a `driver` and `mechanic`.
- **Expected/Actual Result**: Initially raises a `ValueError` when only a mechanic and scout are registered. After dynamically registering a driver, the mission successfully transitions to "In Progress".

### Scenario 5: Testing Custom Modules (Garage & Rivalry)
- **Modules Involved**: Registration, Crew Management, Inventory, Race Management, Garage, Rivalry
- **Description**: Verifies that a registered mechanic can consume inventory parts/tools to repair a heavily damaged car back to 100%. Then tests whether pushing a rival crew's heat past 80 successfully forces interference on an active race, increasing its difficulty tier.
- **Expected/Actual Result**: Car is repaired using logic that properly consumes exact part amounts; rivalry correctly alerts and modifies the race difficulty state by exactly +1.

## Call Graph Implementation Details
*Refer strictly to the hand-drawn Call Graph (Subpart 2.1) in `diagrams/` for a visual mapping of the Python function invocations between these modules.*
