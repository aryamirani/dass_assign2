class RaceManagement:
    """
    Module 4: Race Management
    Creates races and selects appropriate drivers and cars from the system.
    """
    def __init__(self, crew_mgr, inventory):
        self.crew = crew_mgr
        self.inventory = inventory
        self.races = {}  # race_id -> dict with details
        
    def create_race(self, race_id, difficulty):
        """Creates a new race event with a given difficulty multiplier."""
        if race_id in self.races:
            raise ValueError(f"Race '{race_id}' already exists.")
        if difficulty < 1:
            raise ValueError("Difficulty must be at least 1.")
            
        self.races[race_id] = {
            "difficulty": difficulty,
            "participants": [],
            "completed": False
        }
        print(f"Race '{race_id}' created with difficulty {difficulty}.")
        return True
        
    def enter_race(self, race_id, driver_name, car_name):
        """Registers a driver and car for an upcoming race. Enforces business rules."""
        if race_id not in self.races:
            raise ValueError(f"Race '{race_id}' not found.")
        if self.races[race_id]["completed"]:
            raise ValueError(f"Race '{race_id}' has already been completed.")
            
        # Check driver role business rule
        driver_roles = self.crew.get_crew_by_role("driver")
        if driver_name not in driver_roles:
            raise ValueError(f"Crew member '{driver_name}' is not a registered driver.")
            
        # Check car availability and condition business rule
        car_condition = self.inventory.get_car_condition(car_name)
        if car_condition is None:
            raise ValueError(f"Car '{car_name}' not found in inventory.")
        if car_condition < 20: 
            raise ValueError(f"Car '{car_name}' is too damaged to race (Condition: {car_condition}%).")
            
        self.races[race_id]["participants"].append({
            "driver": driver_name,
            "car": car_name
        })
        print(f"Driver '{driver_name}' entered race '{race_id}' with car '{car_name}'.")
        return True
