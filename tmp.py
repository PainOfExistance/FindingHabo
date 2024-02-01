from asset_loader import AssetLoader

assets=AssetLoader()

world=assets.load_level_data()

entities = {
    "Player_spawn": [],
    "Enemy_Random_Spawn": [],
    "Item_field": [],
    "Container_field": [],
    "Metadata": []
}

for entity_type, entity_list in world["entities"].items():
    for entity in entity_list:
        if entity_type == "Player_spawn":
            entities["Player_spawn"].append(entity)
        elif entity_type == "Enemy_Random_Spawn":
            entities["Enemy_Random_Spawn"].append(entity)
        elif entity_type == "Item_field":
            entities["Item_field"].append(entity)
        elif entity_type == "Container_field":
            entities["Container_field"].append(entity)
        elif entity_type == "Metadata":
            entities["Metadata"].append(entity)

print(entities["Player_spawn"])