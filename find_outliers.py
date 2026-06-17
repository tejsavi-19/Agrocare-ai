import cv2
import os
import numpy as np

def find_bright_outliers(folder_path, threshold=65):
    print(f"\nSearching for bright images in: {folder_path} (Threshold: {threshold})")
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    bright_files = []
    
    for f in files:
        path = os.path.join(folder_path, f)
        img = cv2.imread(path)
        if img is None: continue
        
        # Mean intensity of Green channel (index 1 in BGR)
        mean_green = np.mean(img[:,:,1])
        
        if mean_green > threshold:
            bright_files.append((f, mean_green))
            
    print(f"Found {len(bright_files)} images above threshold.")
    for f, val in sorted(bright_files, key=lambda x: x[1], reverse=True)[:20]:
        print(f"File: {f}, Green Mean: {val:.2f}")
    
    return bright_files

if __name__ == "__main__":
    healthy_path = "Plant dataset/leaves_healthy_or_diseased/healthy"
    find_bright_outliers(healthy_path)
    
    diseased_path = "Plant dataset/leaves_healthy_or_diseased/diseased"
    find_bright_outliers(diseased_path, threshold=65)
