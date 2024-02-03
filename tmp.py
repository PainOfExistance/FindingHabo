import time
from datetime import datetime, timedelta


class CustomDate:
    def __init__(self):
        # Define custom month names
        self.custom_month_names = {
            1: "Shining Dawn",  # January
            2: "Dry Cut",  # February
            3: "Earth Cultivation",  # March
            4: "Small Grass",  # April
            5: "Large Grass",  # May
            6: "Flowers",  # June
            7: "Small Sickle",  # July
            8: "Large Sickle",  # August
            9: "Nodding Fruit",  # September
            10: "Wine Flowing",  # October
            11: "Falling Leaves",  # November
            12: "Biting Cold",  # December
        }
        # Set the starting date
        self.start_date = datetime(1945, 5, 9)
        self.start_date = self.start_date.replace(hour=9, minute=42, second=36)
        self.current_date=self.start_date

    def increment_seconds(self):
        # Calculate the elapsed time since the start date
        # elapsed_time = time.time() - self.start_date.timestamp()
        # Add the elapsed time to the start date
        self.current_date = self.current_date + timedelta(seconds=1)

    def print_date(self):
        # Replace the month number with the custom month name
        custom_month_name = self.custom_month_names[self.current_date.month]
        # Print the date with the custom month name and year
        print(f"{self.current_date.day}.{custom_month_name}.{self.current_date.year}   {self.current_date.hour}:{self.current_date.minute}:{self.current_date.second}")


# Create an instance of the class
my_date = CustomDate()

# Increment seconds
my_date.increment_seconds()

# Print the date with the custom month name
my_date.print_date()
