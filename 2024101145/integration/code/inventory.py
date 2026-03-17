class Inventory:
    """
    Module 3: Inventory
    Tracks cars, spare parts, tools, and the cash balance.
    """
    def __init__(self, starting_cash=10000):
        self.cars = {}  # name -> condition (0-100)
        self.spare_parts = 0
        self.tools = 0
        self.cash_balance = starting_cash

    def add_car(self, car_name, condition=100):
        """Adds a car to the inventory."""
        if not car_name:
            raise ValueError("Car name cannot be empty.")
        if car_name in self.cars:
            raise ValueError(f"Car '{car_name}' already exists in inventory.")
            
        self.cars[car_name] = max(0, min(100, condition))
        print(f"Added car '{car_name}' (Condition: {self.cars[car_name]}%)")
        return True

    def get_car_condition(self, car_name):
        return self.cars.get(car_name)

    def damage_car(self, car_name, damage_amount):
        """Reduces the condition of a specific car."""
        if car_name not in self.cars:
            raise ValueError(f"Car '{car_name}' not found.")
        
        self.cars[car_name] = max(0, self.cars[car_name] - damage_amount)
        print(f"Car '{car_name}' took {damage_amount}% damage. New condition: {self.cars[car_name]}%")

    def add_supplies(self, parts=0, tools=0):
        self.spare_parts += parts
        self.tools += tools

    def use_supplies(self, parts=0, tools=0):
        if self.spare_parts < parts or self.tools < tools:
            raise ValueError("Not enough supplies in inventory.")
        self.spare_parts -= parts
        self.tools -= tools

    def update_cash(self, amount):
        """Adds positive or negative cash strictly tracking the crew's bank."""
        if self.cash_balance + amount < 0:
            raise ValueError("Insufficient cash balance.")
        self.cash_balance += amount
        print(f"Inventory cash flow: ${amount}. New balance: ${self.cash_balance}.")
        return self.cash_balance
