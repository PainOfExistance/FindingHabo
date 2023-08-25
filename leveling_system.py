import pygame
import numpy as np
from traits import Traits

class LevelingSystem:
    def __init__(self, assets):
        self.level = 1
        self.experience = 0
        self.required_experience = 100
        self.traits = Traits(assets)

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.required_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.traits.unused_trait_points =+ 2
        self.experience -= self.required_experience
        self.required_experience = self.calculate_next_required_experience(self.level)
        
    def calculate_next_required_experience(self, current_level):
        base_experience = 100
        experience_increment = 50
        increment_multiplier = 1.1 
        return int(base_experience + (experience_increment * (increment_multiplier ** (current_level - 2))))
    
    def draw(self, screen, selected_sub_item, sub_items):
        trait_font = pygame.font.Font("inter.ttf", 24)
        item_spacing = 40
        i=0
        coords=(screen.get_width()+screen.get_width()//4) / 2
        
        scroll_position = (selected_sub_item // 2) * 2
        visible_items = list(self.traits.traits.items())[scroll_position : scroll_position + 2]
        for index, (trait_name, trait_data) in enumerate(
            visible_items
        ):
            color = (
                (157, 157, 210)
                if index == selected_sub_item - scroll_position
                else (237, 106, 94)
                if sub_items
                else (120, 120, 120)
            )
            print(f"   index: {index}")
            print(f"selected: {selected_sub_item}")
            
            if index == selected_sub_item - scroll_position:
                item_text = f"> {trait_name} dexcription: {trait_data['description']} levels: {trait_data['levels']}"
            else:
                item_text = f"    {trait_name} dexcription: {trait_data['description']} levels: {trait_data['levels']}"
            
            for x in trait_data:
                #print(trait_data[x])

                
                if x=="name" or x=="description":
                    item_render = trait_font.render(f"{trait_data[x]}", True, color)
                    item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                    screen.blit(item_render, item_rect)
                    i += item_spacing
                elif x=="levels":
                    txt=f""
                    pwr=f""
                    lvl=f""
                    for z in range(len(trait_data[x])):
                        txt+=f"|{trait_data[x][z]['level']}" 
                        tmp=f"●|" if trait_data[x][z]['taken'] else f"○|"
                        txt+=f"{tmp}"
                        lvl+=f"|{trait_data[x][z]['effect']}|"
                        
                    item_render = trait_font.render(txt, True, color)
                    item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                    screen.blit(item_render, item_rect)
                    i += item_spacing
                    
                    item_render = trait_font.render(lvl, True, color)
                    item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                    screen.blit(item_render, item_rect)
                    i += item_spacing