import os
import shutil
from random import shuffle

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def split_data(source_images, source_labels, dest_paths, train_ratio=0.7):
    images = [f for f in os.listdir(source_images) if f.endswith('.tif')]
    labels = [f for f in os.listdir(source_labels) if f.split('.')[0] in [img.split('.')[0] for img in images]]

    combined = list(zip(images, labels))
    shuffle(combined)

    split_idx = int(len(combined) * train_ratio)
    train_data = combined[:split_idx]
    validate_data = combined[split_idx:]

    for data, data_type in zip([train_data, validate_data], ['train', 'val']):
        img_dest_path = os.path.join(dest_paths['images'], data_type)
        label_dest_path = os.path.join(dest_paths['labels'], data_type)
        ensure_dir(img_dest_path)
        ensure_dir(label_dest_path)

        for img, label in data:
            try:
                shutil.copy(os.path.join(source_images, img), img_dest_path)
                shutil.copy(os.path.join(source_labels, label), label_dest_path)
                print(f"Copied {img} and {label} to {data_type} folders.")
            except Exception as e:
                print(f"Error copying {img} and {label}: {e}")

# Specify your directories
source_images = r'C:\Users\sraad\OneDrive\Documents\project\temp\images\augmented'
source_labels = r'C:\Users\sraad\OneDrive\Documents\project\temp\labels'

dest_paths = {
    'images': r'C:\Users\sraad\OneDrive\Documents\project\data\images',
    'labels': r'C:\Users\sraad\OneDrive\Documents\project\data\labels'
}

split_data(source_images, source_labels, dest_paths)
