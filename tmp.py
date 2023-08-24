class LevelingSystem:
    def __init__(self):
        self.level = 1
        self.experience = 0
        self.required_experience = 100

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.required_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= self.required_experience
        self.required_experience = self.calculate_next_required_experience(self.level)
        
    def calculate_next_required_experience(self, current_level):
        base_experience = 100  # The initial experience required for level 2
        experience_increment = 50  # The initial increment amount
        increment_multiplier = 1.5  # The rate at which the increment increases per level
        return int(base_experience + (experience_increment * (increment_multiplier ** (current_level - 2))))

# In your main game loop or player class:
leveling_system = LevelingSystem()

# When the player gains experience, call the gain_experience method:
leveling_system.gain_experience(50)

for level in range(2, 100):
    required_experience = leveling_system.calculate_next_required_experience(level)
    print(f"Level {level}: {required_experience} experience")