import os
import random
import rasterio
from rasterio.windows import Window

def clip_random_patch(input_path, output_path, patch_size):

    with rasterio.open(input_path) as src:
        width, height = src.width, src.height
        patch_width, patch_height = patch_size
        
        # Ensure the patch is within bounds
        max_x = width - patch_width
        max_y = height - patch_height
        x_offset = random.randint(0, max_x)
        y_offset = random.randint(0, max_y)

        window = Window(x_offset, y_offset, patch_width, patch_height)
        transform = src.window_transform(window)

        # Read the patch
        patch = src.read(window=window)

        # Update the metadata
        metadata = src.meta.copy()
        metadata.update({
            "driver": "GTiff",
            "height": patch_height,
            "width": patch_width,
            "transform": transform
        })

        # Save the patch with metadata
        with rasterio.open(output_path, 'w', **metadata) as dst:
            dst.write(patch)

def process_images(input_dir, output_dir, patch_size):
   
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    images = [f for f in os.listdir(input_dir) if f.endswith('.tif')]
    for i, image_name in enumerate(images, start=1):
        input_path = os.path.join(input_dir, image_name)
        output_path = os.path.join(output_dir, f'clip_{i}.tif')
        clip_random_patch(input_path, output_path, patch_size)
        print(f"Processed {input_path} -> {output_path}")


input_dir = '/Users/kavindev/Desktop/444x444 images'  # Directory containing original images
output_dir = '/Users/kavindev/Desktop/224x224 images'  # Directory to save clipped patches
patch_size = (224, 224)  # Patch size in pixels

process_images(input_dir, output_dir, patch_size)
print("All images have been processed and patches saved to the output directory.")
