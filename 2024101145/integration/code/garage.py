class Garage:
    """
    Custom Module 1: Garage
    Allows mechanics to repair damaged cars using inventory supplies.
    Integrating Crew Management and Inventory.
    """
    def __init__(self, crew_mgr, inventory):
        self.crew = crew_mgr
        self.inventory = inventory
        
    def repair_car(self, car_name, parts_needed=1, tools_needed=1):
        """
        Repairs a damaged car to 100% condition if a mechanic is available and supplies exist.
        """
        mechanics = self.crew.get_crew_by_role("mechanic")
        if not mechanics:
            raise ValueError("No mechanics registered. Cannot authorize repairs.")
            
        car_condition = self.inventory.get_car_condition(car_name)
        if car_condition is None:
            raise ValueError(f"Car '{car_name}' not found in inventory.")
            
        if car_condition == 100:
            return "Car is already in perfect condition."
            
        # Try to consume supplies (will raise ValueError if not enough)
        self.inventory.use_supplies(parts=parts_needed, tools=tools_needed)
        
        # Repair the car
        old_condition = car_condition
        self.inventory.cars[car_name] = 100
        
        mechanic_name = mechanics[0] # Dispatch the first available mechanic
        message = (
            f"Mechanic {mechanic_name} repaired '{car_name}' from "
            f"{old_condition}% to 100% using {parts_needed} parts and {tools_needed} tools."
        )
        print(message)
        return message
