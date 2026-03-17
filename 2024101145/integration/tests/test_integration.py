import pytest
from registration import Registration
from crew_management import CrewManagement
from inventory import Inventory
from race_management import RaceManagement
from results import Results
from mission_planning import MissionPlanning
from garage import Garage
from rivalry import Rivalry

@pytest.fixture
def system():
    reg = Registration()
    crew = CrewManagement(reg)
    inv = Inventory(starting_cash=10000)
    race = RaceManagement(crew, inv)
    res = Results(race, inv)
    mission = MissionPlanning(crew, inv)
    garage = Garage(crew, inv)
    rivalry = Rivalry(race)
    return {
        "reg": reg, "crew": crew, "inv": inv, "race": race, 
        "res": res, "mission": mission, "garage": garage, "rivalry": rivalry
    }

def test_register_and_enter_race(system):
    """Scenario: Registering a driver and entering them into a race."""
    sys = system
    
    # Register and assign
    sys["reg"].register_member("Dominic", "driver")
    sys["crew"].assign_skill("Dominic", 95)
    
    # Inventory setup
    sys["inv"].add_car("Charger", 100)
    
    # Create and enter race
    sys["race"].create_race("Race1", difficulty=1)
    result = sys["race"].enter_race("Race1", "Dominic", "Charger")
    
    assert result is True
    assert len(sys["race"].races["Race1"]["participants"]) == 1
    assert sys["race"].races["Race1"]["participants"][0]["driver"] == "Dominic"

def test_enter_race_without_registered_driver(system):
    """Scenario: Attempting to enter a race without a registered driver."""
    sys = system
    
    sys["inv"].add_car("Skyline", 100)
    sys["race"].create_race("Race2", difficulty=2)
    
    # 'Brian' is not registered
    with pytest.raises(ValueError, match="is not a registered driver"):
        sys["race"].enter_race("Race2", "Brian", "Skyline")

def test_complete_race_and_verify_results(system):
    """Scenario: Completing a race and verifying results and prize money update the inventory."""
    sys = system
    
    sys["reg"].register_member("Letty", "driver")
    sys["crew"].assign_skill("Letty", 90)
    sys["inv"].add_car("Interceptor", 100)
    
    sys["race"].create_race("Race3", difficulty=3)
    sys["race"].enter_race("Race3", "Letty", "Interceptor")
    
    initial_cash = sys["inv"].cash_balance
    prize = sys["res"].record_race_result("Race3", "Letty")
    
    # Verify cash updated
    assert sys["inv"].cash_balance == initial_cash + prize
    assert prize == 15000 # 5000 * difficulty(3)
    
    # Verify car took damage
    assert sys["inv"].get_car_condition("Interceptor") < 100
    
    # Verify leaderboard
    assert sys["res"].leaderboard["Letty"] == 10

def test_assign_mission_role_validation(system):
    """Scenario: Assigning a mission and ensuring correct crew roles are validated."""
    sys = system
    
    sys["reg"].register_member("Tej", "mechanic")
    sys["reg"].register_member("Roman", "scout")
    sys["crew"].assign_skill("Tej", 85)
    
    # Attempting to assign without a driver
    with pytest.raises(ValueError, match="Required role 'driver' is unavailable"):
        sys["mission"].assign_mission("Heist", ["driver", "mechanic"])
        
    # Registering driver fixes it
    sys["reg"].register_member("Han", "driver")
    result = sys["mission"].assign_mission("Heist", ["driver", "mechanic"])
    
    assert result is True
    assert "Heist" in sys["mission"].active_missions

def test_custom_modules_garage_and_rivalry(system):
    """Scenario: Testing Garage repairs and Rivalry race interference."""
    sys = system
    
    # Garage Setup
    sys["reg"].register_member("Mia", "mechanic")
    sys["inv"].add_car("Supra", 40)
    sys["inv"].add_supplies(parts=5, tools=5)
    
    # Repair supra
    sys["garage"].repair_car("Supra", parts_needed=2, tools_needed=1)
    assert sys["inv"].get_car_condition("Supra") == 100
    assert sys["inv"].spare_parts == 3
    
    # Rivalry Setup
    sys["reg"].register_member("Vince", "driver")
    sys["race"].create_race("Race4", difficulty=2)
    sys["race"].enter_race("Race4", "Vince", "Supra")
    
    # Discover and increase rivalry past 80
    sys["rivalry"].discover_crew("DK's Crew", initial_rivalry=10)
    sys["rivalry"].increase_rivalry("DK's Crew", 80) # total 90
    
    # Check interference
    interference = sys["rivalry"].check_race_interference("Race4")
    assert interference is True
    assert sys["race"].races["Race4"]["difficulty"] == 3 # Increased by 1
