from PIL import Image
import math

def apply_halftone(image, strength=1.0, grid_size=4, scale=1.0, shift=0, dot_color=(0, 0, 0), bg_color=(255, 255, 255), gamma=1.0):
    """Apply halftone effect to the image."""
    # Convert image to RGB if it's not
    
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            # Get original RGB
            original_r, original_g, original_b, alpha = pixels[x, y]
            
            # Calculate luminance
            luminance = (0.298912 * original_r + 0.586611 * original_g + 0.114478 * original_b) / 255
            
            # Calculate grid position
            grid_x = (x + shift) % grid_size
            grid_y = (y + shift) % grid_size
            
            # Calculate distance to the nearest grid center
            dist = math.sqrt(grid_x**2 + grid_y**2) * grid_size
            
            # Calculate dot size
            dot_size = (1 - luminance**gamma) * scale * grid_size
            
            # Determine the ratio of the dot color to the background color
            ratio = min(1, max(0, strength * (1 - (dist - dot_size))))
            
            # Blend the dot color and the background color
            new_r = ratio * dot_color[0] + (1 - ratio) * bg_color[0]
            new_g = ratio * dot_color[1] + (1 - ratio) * bg_color[1]
            new_b = ratio * dot_color[2] + (1 - ratio) * bg_color[2]
            
            # Place new pixel
            pixels[x, y] = (int(new_r), int(new_g), int(new_b), alpha)

    return image

file_path = input('画像ファイルのパスを入力してください: ')


# Load an image
input_image = Image.open(file_path)

# Apply halftone effect
output_image = apply_halftone(input_image, strength=1.0, grid_size=4, scale=100, shift=0, dot_color=(0,0,0), bg_color=(255,255,255), gamma=0.04)

# Save the output
output_image.save(f'halftone_{file_path}')
