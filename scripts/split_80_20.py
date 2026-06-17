import os
import random
import shutil

def split(src, dst, ratio=0.2):
    files = [f for f in os.listdir(src) if f.lower().endswith((".jpg",".jpeg",".png"))]
    random.shuffle(files)

    n = int(len(files) * ratio)

    os.makedirs(dst, exist_ok=True)

    for f in files[:n]:
        shutil.move(os.path.join(src, f), os.path.join(dst, f))

split("dataset/train/Healthy", "dataset/val/Healthy")
split("dataset/train/Diseased", "dataset/val/Diseased")

print("80/20 split completed.")
