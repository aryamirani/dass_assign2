class MissionPlanning:
    """
    Module 6: Mission Planning
    Assigns missions (e.g., delivery, rescue) and verifies required roles are available.
    """
    def __init__(self, crew_mgr, inventory):
        self.crew = crew_mgr
        self.inventory = inventory
        self.active_missions = {}
        
    def assign_mission(self, mission_name, required_roles, required_car_condition=0):
        """
        Starts a mission if the required crew roles are available and minimum inventory requirements are met.
        required_roles: list of string roles e.g. ["driver", "mechanic", "scout"]
        """
        if mission_name in self.active_missions:
            raise ValueError(f"Mission '{mission_name}' is already active.")
            
        # Business Rule: Verify required roles are available
        assigned_members = []
        for role in required_roles:
            potential_members = self.crew.get_crew_by_role(role)
            if not potential_members:
                raise ValueError(
                    f"Cannot start mission '{mission_name}'. "
                    f"Required role '{role}' is unavailable in the crew."
                )
            # Just take the first available for simplicity in integration
            assigned_members.append(potential_members[0])
            
        # Business rule: check if they have at least one car meeting the condition (e.g. for getaway)
        if required_car_condition > 0:
            usable_car = False
            for car, condition in self.inventory.cars.items():
                if condition >= required_car_condition:
                    usable_car = True
                    break
            if not usable_car:
                raise ValueError(
                    f"Mission '{mission_name}' requires a car with at least "
                    f"{required_car_condition}% condition, but none exist."
                )
                
        self.active_missions[mission_name] = {
            "status": "In Progress",
            "assigned_crew": assigned_members
        }
        
        print(f"Mission '{mission_name}' started successfully with crew: {assigned_members}.")
        return True
