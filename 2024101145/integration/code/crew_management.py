class CrewManagement:
    """
    Module 2: Crew Management
    Manages roles (e.g., driver, mechanic, strategist) and records skill levels for each.
    """
    def __init__(self, registration_mgr):
        self.registration = registration_mgr
        self.skills = {}  # name -> skill_level (int 1-100)
    
    def assign_skill(self, name, skill_level):
        """Assigns a skill level (1-100) to a registered crew member."""
        if not self.registration.is_registered(name):
            raise ValueError(f"Cannot assign skill: '{name}' is not a registered crew member.")
            
        if not isinstance(skill_level, int) or not (1 <= skill_level <= 100):
            raise ValueError("Skill level must be an integer between 1 and 100.")
            
        self.skills[name] = skill_level
        print(f"Assigned skill level {skill_level} to {name}.")
        return True
        
    def get_skill(self, name):
        """Gets the recorded skill level of a crew member."""
        if not self.registration.is_registered(name):
            raise ValueError(f"Crew member '{name}' not found.")
        return self.skills.get(name, 0) # Base skill is 0 if unassigned

    def get_crew_by_role(self, role, required_skill=0):
        """Returns a list of crew member names having the specific role and minimum skill."""
        qualified = []
        for name, r in self.registration.registered_members.items():
            if r == role.lower():
                if self.get_skill(name) >= required_skill:
                    qualified.append(name)
        return qualified
