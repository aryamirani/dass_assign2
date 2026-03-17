class Registration:
    """
    Module 1: Registration
    Registers new crew members, storing name and role.
    """
    def __init__(self):
        self.registered_members = {}  # name -> role

    def register_member(self, name, role):
        """Registers a crew member with a specific role."""
        if not name or not role:
            raise ValueError("Name and role must be provided.")
        if name in self.registered_members:
            raise ValueError(f"Crew member '{name}' is already registered.")
        
        valid_roles = ["driver", "mechanic", "strategist", "scout"]
        if role.lower() not in valid_roles:
            raise ValueError(f"Role '{role}' is invalid. Must be one of {valid_roles}.")
            
        self.registered_members[name] = role.lower()
        print(f"Registered {name} as {role.lower()}.")
        return True

    def is_registered(self, name):
        """Checks if a crew member is registered."""
        return name in self.registered_members

    def get_role(self, name):
        """Gets the role of a registered crew member."""
        return self.registered_members.get(name)
