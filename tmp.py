import json
import numpy as np

item_list=np.array({})
with open("items.json", "r") as items:
    item_list = json.load(items)["items"]

for item in item_list:
    print(item["effect"]["name"])