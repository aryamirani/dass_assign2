import random

class Results:
    """
    Module 5: Results
    Records race outcomes, updates rankings, and handles prize money.
    """
    def __init__(self, race_mgr, inventory):
        self.race_mgr = race_mgr
        self.inventory = inventory
        self.leaderboard = {}  # driver_name -> total points
        
    def record_race_result(self, race_id, winner_name):
        """Processes the aftermath of a race, updating cash, damage, and rankings."""
        if race_id not in self.race_mgr.races:
            raise ValueError(f"Race '{race_id}' not found.")
        if self.race_mgr.races[race_id]["completed"]:
            raise ValueError(f"Race '{race_id}' already has recorded results.")
            
        participants = self.race_mgr.races[race_id]["participants"]
        
        if not participants:
            raise ValueError(f"Cannot record result: No participants in race '{race_id}'.")
            
        driver_entry = None
        for p in participants:
            if p["driver"] == winner_name:
                driver_entry = p
                break
                
        if not driver_entry:
            raise ValueError(f"Driver '{winner_name}' did not participate in race '{race_id}'.")
            
        # Update leaderboard points for the winner
        self.leaderboard[winner_name] = self.leaderboard.get(winner_name, 0) + 10
        
        # Calculate and award prize money based on difficulty business rule
        difficulty = self.race_mgr.races[race_id]["difficulty"]
        prize = 5000 * difficulty
        self.inventory.update_cash(prize)
        
        # Simulate damage to participated cars (Integration overlap)
        for p in participants:
            # 5% to 25% damage randomly
            damage = random.randint(5, 25)
            # Higher difficulty = more potential damage
            damage += (difficulty * 2)
            self.inventory.damage_car(p["car"], damage)
            
        self.race_mgr.races[race_id]["completed"] = True
        print(f"Recorded results for '{race_id}'. Winner: {winner_name} (+10 pts). Prize: ${prize}.")
        return prize
