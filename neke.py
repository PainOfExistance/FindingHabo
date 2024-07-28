import os
import re
from math import sqrt

import cv2
import numpy as np


# Function to find and process folders
def process_folders(base_folder):
    # Dictionary to store images
    images_dict = {}
    # Regex pattern to match folder names
    pattern = re.compile(r"Kiavar_(\d+)x(\d+)")

    # Walk through all folders in the base folder
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            match = pattern.match(dir_name)
            if match:
                # Extract coordinates from the folder name
                x, y = int(match.group(1)), int(match.group(2))
                # Initialize dictionary for each image type
                images_dict[(x, y)] = {}

                # Path to the current folder
                folder_path = os.path.join(root, dir_name)
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(".png"):
                        img_path = os.path.join(folder_path, file_name)
                        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                        
                        if "Animator_" in file_name:
                            img = cv2.resize(img, (5256, 5256), interpolation = cv2.INTER_AREA)
                        elif "Collision-" in file_name:
                            img = cv2.resize(img, (5256, 5256), interpolation = cv2.INTER_AREA)
                            
                        images_dict[(x, y)][file_name] = img[:5248, :5248]
    
    return images_dict

def create_image_grid(images_dict, grid_size, output_folder):
    images = {}
    for (x, y), data in images_dict.items():
        for key in data:
            image = data[key]
            print(key, image.shape)
            if key not in images:
                images[key] = np.zeros((grid_size * 5248, grid_size * 5248, 4), dtype=np.uint8)
            x_offset = x * 5248
            y_offset = y * 5248
            images[key][y_offset:y_offset+5248, x_offset:x_offset+5248] = image
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for key, grid_image in images.items():
        cv2.imwrite(os.path.join(output_folder, key), grid_image)

# Main function
def main():
    base_folder = "terrain/worlds_exter/simplified"
    output_folder = os.path.join(base_folder, "Kiavar")
    
    # Process the folders and get images
    images_dict = process_folders(base_folder)
    
    # Assuming grid size is 10x10
    grid_size = int(sqrt(len(images_dict)))
    
    # Create and save the merged image grids
    create_image_grid(images_dict, grid_size, output_folder)

if __name__ == "__main__":
    main()
