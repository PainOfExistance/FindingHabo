import time
from datetime import datetime, timedelta


class GameDate:
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
        start_date = datetime(1945, 5, 9)
        start_date = start_date.replace(hour=8, minute=42, second=36)
        self.current_date=start_date

    def increment_seconds(self):
        # Calculate the elapsed time since the start date
        # elapsed_time = time.time() - self.start_date.timestamp()
        # Add the elapsed time to the start date
        self.current_date = self.current_date + timedelta(seconds=1)

    def print_date(self):
        # Replace the month number with the custom month name
        custom_month_name = self.custom_month_names[self.current_date.month]
        weekday_name = self.current_date.strftime("%A")  # Get the full weekday name
        day_of_month = self.current_date.day  # Get the day of the month
        hour = self.current_date.hour  # Get the hour
        minute = self.current_date.minute  # Get the minute
        custom_month_name = self.custom_month_names[self.current_date.month]  # Get the custom month name
        year = f"{str(self.current_date.year)[0]}E A{str(self.current_date.year)[1:4]}"  # Get the year
        formatted_str = f"{weekday_name} {hour:02d}.{minute:02d}, {day_of_month}th of {custom_month_name} of {year}"
        return formatted_str

    def get_date(self):
        return self.current_date.isoformat()
    
    def to_dict(self):
        return {
            "current_date": self.current_date.isoformat()
        }

    def from_dict(self, data):
        self.current_date = datetime.fromisoformat(data["current_date"])