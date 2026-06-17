import cv2
import numpy as np

def test_logic():
    # Create a dummy heatmap (224x224)
    heatmap = np.zeros((224, 224), dtype=np.float32)
    # Add a "hot" spot
    heatmap[50:100, 50:100] = 0.8
    
    # Original image (dummy)
    img = np.zeros((224, 224, 3), dtype=np.uint8) + 128 # Gray image
    
    # 1. Threshold
    threshold_value = 0.5
    binary_mask = np.uint8(heatmap > threshold_value) * 255
    
    # 2. Find contours
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 3. Draw red outline
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        print(f"Success: Detected region at [{x}, {y}, {w}, {h}]")
        
        # Check color at (x+2, y+2) - should be red (0, 0, 255) in BGR
        # Wait, the rectangle border is at (x, y). Let's check (x, y)
        pixel_color = img[y, x]
        print(f"Color at boundary: {pixel_color}")
        if np.array_equal(pixel_color, [0, 0, 255]):
            print("Color check passed: Red (0, 0, 255)")
        else:
            print(f"Color check failed: {pixel_color}")
    else:
        print("Failed: No contours found")

if __name__ == "__main__":
    test_logic()
