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
        text_y = 20
        i=0
        for index, (trait_name, trait_data) in enumerate(
            self.traits.traits.items()
        ):
            color = (
                (157, 157, 210)
                if index == selected_sub_item
                else (237, 106, 94)
                if sub_items
                else (120, 120, 120)
            )
            
            if index == selected_sub_item:
                item_text = f"> {trait_name} dexcription: {trait_data['description']} levels: {trait_data['levels']}"
            else:
                item_text = f"    {trait_name} dexcription: {trait_data['description']} levels: {trait_data['levels']}"
            
            for x in trait_data:
                #print(trait_data[x])

                coords=(screen.get_width()+screen.get_width()//4) / 2
                
                if x=="name" or x=="description":
                    item_render = trait_font.render(f"{trait_data[x]}", True, color)
                    item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                    screen.blit(item_render, item_rect)
                    text_y += item_spacing
                    i += item_spacing
                elif x=="levels":
                    txt=f""
                    for z in range(len(trait_data[x])):
                        txt+=f"|{trait_data[x][z]['level']} {trait_data[x][z]['effect']} {trait_data[x][z]['taken']}| "
                        
                    item_render = trait_font.render(txt, True, color)
                    item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                    screen.blit(item_render, item_rect)
                    text_y += item_spacing
                    i += item_spacing
                        