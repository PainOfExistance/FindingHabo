import imageio
from PIL import Image


def is_mostly_red(tile):
    if tile.mode!= "RGBA":  # Ensure the tile supports transparency
        tile = tile.convert("RGBA")
    
    width, height = tile.size
    total_pixels = width * height
    red_pixels = sum(
        1 for x in range(width) for y in range(height) 
        if tile.getpixel((x, y))[0] > 200 and tile.getpixel((x, y))[1] < 50 and tile.getpixel((x, y))[2] < 50  # Red pixel
    )
    
    # Consider the tile as a blocker if more than 90% of its pixels are red
    return red_pixels > (total_pixels * 0.9)

def generate_multiple_gifs_from_sprite_sheet(sprite_sheet_path, base_output_name):
    sprite_sheet = Image.open(sprite_sheet_path)
    frames = []
    tile_width, tile_height = 16, 16
    gif_index = 0
    tile_count = 0  # Counter to keep track of processed tiles
    
    for y in range(0, sprite_sheet.height, tile_height):
        for x in range(0, sprite_sheet.width, tile_width):
            tile = sprite_sheet.crop((x, y, x + tile_width, y + tile_height))
            
            if is_mostly_red(tile):
                # Skip saving the current GIF if the tile is red
                if frames:
                    output_gif_path = f"out/{base_output_name}_{gif_index}.gif"
                    # Using Pillow to save the GIF with APNG_DISPOSE_OP_BACKGROUND
                    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0, disposal=1)
                    gif_index += 1
                    frames.clear()
            elif tile_count % 5!= 4:  # Process every tile except the fifth one in each group
                frames.append(tile)
                tile_count += 1
            else:
                tile_count += 1  # Increment counter even for skipped tiles
                
            if len(frames) == 4:  # When 4 tiles are collected, save them as a GIF
                output_gif_path = f"out/{base_output_name}_{gif_index}.gif"
                # Using Pillow to save the GIF with APNG_DISPOSE_OP_BACKGROUND
                frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0, disposal=1)
                gif_index += 1
                frames.clear()

    # Save the last GIF if there are remaining frames
    if frames:
        output_gif_path = f"out/{base_output_name}_{gif_index}.gif"
        # Using Pillow to save the GIF with APNG_DISPOSE_OP_BACKGROUND
        frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0, disposal=1)

# Example usage
generate_multiple_gifs_from_sprite_sheet('tmp.png', 'output')
