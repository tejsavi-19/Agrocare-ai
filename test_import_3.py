try:
    from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
    print("Import preprocess_input successful via tensorflow.keras.applications.mobilenet_v3")
except ImportError:
    print("Import preprocess_input failed via tensorflow.keras.applications.mobilenet_v3")

try:
    from tensorflow.keras.applications import mobilenet_v3
    print("Import mobilenet_v3 module successful via tensorflow.keras.applications")
except ImportError:
    print("Import mobilenet_v3 module failed via tensorflow.keras.applications")
