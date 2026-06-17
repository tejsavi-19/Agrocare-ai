"""
Validate and fix corrupt images in the dataset
"""

import os
from PIL import Image
import shutil

def validate_images(dataset_path='dataset'):
    """
    Check all images in dataset and remove or fix corrupt ones.
    """
    print("=" * 60)
    print("Dataset Validation and Repair")
    print("=" * 60)
    
    corrupt_count = 0
    valid_count = 0
    removed_count = 0
    
    # Check all subdirectories
    for root, dirs, files in os.walk(dataset_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Only check image files
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                continue
            
            try:
                # Try to open and verify the image
                with Image.open(file_path) as img:
                    img.verify()  # This will detect corrupted images
                    # Try to load it again to make sure it's readable
                    with Image.open(file_path) as img2:
                        img2.load()
                valid_count += 1
                print(f"✓ {file_path}")
            except (IOError, OSError, Image.UnidentifiedImageError) as e:
                corrupt_count += 1
                print(f"✗ CORRUPT: {file_path} - {str(e)[:50]}")
                # Remove corrupted image
                try:
                    os.remove(file_path)
                    removed_count += 1
                    print(f"  Removed corrupt image")
                except:
                    print(f"  Could not remove - check permissions")
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"Valid images: {valid_count}")
    print(f"Corrupt images found: {corrupt_count}")
    print(f"Corrupt images removed: {removed_count}")
    print(f"\nDataset is ready for training!" if corrupt_count == removed_count else f"\nWarning: {corrupt_count - removed_count} corrupt images remain")

if __name__ == '__main__':
    validate_images()
