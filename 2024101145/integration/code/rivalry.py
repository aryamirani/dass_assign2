class Rivalry:
    """
    Custom Module 2: Rivalry System
    Tracks heat and rivalry levels with opposing crews. High rivalry can block certain missions
    or increase the difficulty of races against them.
    """
    def __init__(self, race_mgr):
        self.race_mgr = race_mgr
        self.crews = {}  # name -> rivalry_level (1-100)
        
    def discover_crew(self, crew_name, initial_rivalry=10):
        """Registers a new rival crew in the underground network."""
        if not crew_name:
            raise ValueError("Rival crew name cannot be empty.")
            
        if crew_name in self.crews:
            return False
            
        self.crews[crew_name] = max(1, min(100, initial_rivalry))
        print(f"Discovered new rival crew: {crew_name} (Rivalry: {self.crews[crew_name]})")
        return True
        
    def increase_rivalry(self, crew_name, amount):
        """Increases hostility with a rival crew (e.g., after beating them in a race)."""
        if crew_name not in self.crews:
            self.discover_crew(crew_name)
            
        self.crews[crew_name] = min(100, self.crews[crew_name] + amount)
        print(f"Rivalry with {crew_name} increased. Current: {self.crews[crew_name]}")
        
    def decrease_rivalry(self, crew_name, amount):
        """Bribes or alliances can reduce rivalry."""
        if crew_name not in self.crews:
            return
            
        self.crews[crew_name] = max(1, self.crews[crew_name] - amount)
        print(f"Rivalry with {crew_name} decreased. Current: {self.crews[crew_name]}")
        
    def check_race_interference(self, race_id):
        """
        Business Rule Integration: If any rival crew has rivalry > 80, 
        they interfere and increase the race difficulty by 1.
        """
        if race_id not in self.race_mgr.races:
            raise ValueError(f"Race '{race_id}' not found.")
            
        interference = False
        for crew, level in self.crews.items():
            if level > 80:
                print(f"Rival crew '{crew}' is interfering with race '{race_id}'!")
                self.race_mgr.races[race_id]["difficulty"] += 1
                interference = True
                
        return interference
