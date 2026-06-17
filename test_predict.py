import sys
import os
sys.path.append(os.path.abspath(r'C:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\AgroCareAI\backend'))
from ai_engine import ai_engine

if not ai_engine.model:
    print("Model not loaded!")
    sys.exit(1)

# Pick an image from frontend public or backend uploads to test
test_image_paths = [
    r"C:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\test_image.py" # not an image, let's find an image
]
# I will search for a sample image in the directory
import glob
images = glob.glob(r'C:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\AgroCareAI\backend\uploads\*.jpg')
if not images:
    images = glob.glob(r'C:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\AgroCareAI\backend\uploads\*.JPG')

if images:
    print(f"Testing prediction on {images[0]}")
    try:
        res = ai_engine.predict(images[0])
        print("Prediction result:", res)
    except Exception as e:
        print("Exception during predict:", e)
else:
    print("No images found in uploads directory to test.")
