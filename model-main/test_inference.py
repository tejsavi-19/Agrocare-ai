"""
Quick test script to run inference on a single image
"""

from inference_binary_leaf_stem import predict_health
import os
import traceback

# Test image path
test_image = r"C:\Users\USER\Downloads\p2.jpg"

if os.path.exists(test_image):
    print("=" * 60)
    print("Testing Inference on Image")
    print("=" * 60)
    print(f"\nImage: {test_image}")
    
    try:
        result = predict_health(test_image)
        print(f"\nResult:")
        print(f"  Status: {result['status']}")
        print(f"  Confidence: {result['confidence']:.4f}")
        print("\n✓ Inference successful!")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nFull Traceback:")
        traceback.print_exc()
else:
    print(f"✗ Image not found: {test_image}")
