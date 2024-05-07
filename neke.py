import json


def load_routine(filename):
    with open(f"./packages/{filename}.szbc", 'r') as file:
        data = json.load(file)
    return data

def get_actions(day, time, routines):
    actions = []
    hour, _ = map(int, time.split('.'))
    for routine in routines["routines"]:
        for routine_name, schedule in routine.items():
            if day in routines["schedule"][routine_name]:
                closest_hour = min(schedule.keys(), key=lambda x: abs(int(x.split('.')[0]) - hour))
                routine_actions = schedule.get(closest_hour)
                if routine_actions:
                    routine_actions.append(closest_hour)
                    actions.extend(routine_actions)
    return actions

# Example usage
data = load_routine("dream_city_merchant_misc")
actions = get_actions(1, "8.59", data)
print(actions)