import os
import numpy as np
from PIL import Image

# Specify the directories containing the images and the masks
image_dir ="D:/temp/images"
mask_dir = "D:/temp/masks"


from PIL import Image
import os

# Paths to the directories
image_dir = "D:/temp/images"
mask_dir = "D:/temp/masks"

# Loop over each file in the mask directory
for filename in os.listdir(mask_dir):
    if filename.endswith('.png'):  # Ensure processing only PNG files
        base_name = os.path.splitext(filename)[0]  # Remove the file extension
        mask_path = os.path.join(mask_dir, filename)
        image_filename = base_name + '.tif'  # Create the corresponding image file name
        image_path = os.path.join(image_dir, image_filename)

        try:
            # Open the mask and check if it is completely black
            mask = Image.open(mask_path)
            if mask.convert('L').getextrema() == (0, 0):
                # Delete the mask
                os.remove(mask_path)
                print(f"Deleted mask: {filename}")

                # Check if the corresponding image file exists and delete it
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"Deleted corresponding image: {image_filename}")
                else:
                    print(f"No corresponding image found for: {image_filename}")
            else:
                print(f"Mask {filename} is not completely black.")

        except IOError:
            print(f"Cannot open {filename}.")
