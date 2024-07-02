from PIL import Image
import os

# Paths to your images and masks folders
images_path ='/path/to/your/project/directory/'
masks_path = '/path/to/your/project/directory/'

# Create directories for augmented images and masks if they do not exist
augmented_images_path = os.path.join(images_path, 'augmented')
augmented_masks_path = os.path.join(masks_path, 'augmented')
os.makedirs(augmented_images_path, exist_ok=True)
os.makedirs(augmented_masks_path, exist_ok=True)

# Function to apply transformations
def augment_data(file, path, save_to, extension, transformation, angle=None):
    img = Image.open(os.path.join(path, file))
    if angle:
        transformed_img = img.rotate(angle, expand=True)
    else:
        transformed_img = transformation(img)
    transformed_img.save(os.path.join(save_to, f"{transformation.__name__ if not angle else f'rotate_{angle}'}_{file}"), format=extension)

# Define transformations
def flip_left_right(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def flip_top_bottom(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

# Loop through each file in the images directory
for file_name in os.listdir(images_path):
    if file_name.endswith('.tif'):  # Processing TIFF images
        # Horizontal flip
        augment_data(file_name, images_path, augmented_images_path, 'TIFF', flip_left_right)
        # Vertical flip
        augment_data(file_name, images_path, augmented_images_path, 'TIFF', flip_top_bottom)
        # Rotations
        for angle in [90, 180, 270]:
            augment_data(file_name, images_path, augmented_images_path, 'TIFF', Image.Image.rotate, angle)

# Repeat for masks with PNG format
for file_name in os.listdir(masks_path):
    if file_name.endswith('.png'):  # Processing PNG masks
        # Horizontal flip
        augment_data(file_name, masks_path, augmented_masks_path, 'PNG', flip_left_right)
        # Vertical flip
        augment_data(file_name, masks_path, augmented_masks_path, 'PNG', flip_top_bottom)
        # Rotations
        for angle in [90, 180, 270]:
            augment_data(file_name, masks_path, augmented_masks_path, 'PNG', Image.Image.rotate, angle)
