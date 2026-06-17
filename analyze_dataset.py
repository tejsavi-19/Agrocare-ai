import cv2
import os
import numpy as np

def analyze_folder(folder_path):
    print(f"\nAnalyzing: {folder_path}")
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        print("No images found.")
        return

    sample_count = min(10, len(files))
    samples = files[:sample_count]
    
    for f in samples:
        path = os.path.join(folder_path, f)
        img = cv2.imread(path)
        if img is not None:
            h, w, c = img.shape
            # Calculate mean color to check for background bias
            mean_color = np.mean(img, axis=(0, 1))
            print(f"File: {f}, Size: {w}x{h}, Mean Color (BGR): {mean_color}")
        else:
            print(f"File: {f}, Failed to load.")

dataset_root = "Plant dataset/leaves_healthy_or_diseased"
analyze_folder(os.path.join(dataset_root, "healthy"))
analyze_folder(os.path.join(dataset_root, "diseased"))
