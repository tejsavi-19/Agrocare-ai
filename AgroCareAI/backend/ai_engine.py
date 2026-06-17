import os
# Lazy imports for AI libraries to allow app to start without them
tf = None
np = None
torch = None

from config import Config
import base64
from io import BytesIO

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

IMG_SIZE = 224

class AIEngine:
    def __init__(self):
        self.model = None
        self.category_model = None
        self.class_to_idx = None
        self.idx_to_class = None
        self.device = None
        # We'll try to load models, but if imports fail, we won't crash
        try:
            self.load_model()
            self.load_category_model()
        except Exception as e:
            print(f"CRITICAL: Could not initialize AI models: {e}")

    def load_model(self):
        global tf, np
        try:
            import tensorflow as tensorflow_lib
            import numpy as numpy_lib
            tf = tensorflow_lib
            np = numpy_lib
        except ImportError:
            print("WARNING: TensorFlow not found. Prediction features will be disabled.")
            return

        path = Config.MODEL_PATH
        if not os.path.exists(path):
            alt_path = path.replace(".keras", ".h5")
            if os.path.exists(alt_path):
                print(f"DEBUG: .keras not found, falling back to legacy {alt_path}")
                path = alt_path
            else:
                print(f"CRITICAL ERROR: Model file not found at {path}")
                return

        print(f"Loading binary model from {path}...", flush=True)
        try:
            self.model = tf.keras.models.load_model(path, compile=False)
            print("Binary model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            if ".keras" in path:
                alt_path = path.replace(".keras", ".h5")
                if os.path.exists(alt_path):
                    print(f"Attempting fallback to legacy {alt_path}")
                    try:
                        self.model = tf.keras.models.load_model(alt_path, compile=False)
                        print("Fallback success.")
                        return
                    except Exception as fallback_e:
                        print(f"Fallback .h5 model also failed to load: {fallback_e}")
            self.model = None

    def load_category_model(self):
        global torch
        import sys
        # Navigate from model-main2 to TEJU folder
        cat_dir = os.path.join(os.path.dirname(Config.BASE_DIR), 'cat')
        if cat_dir not in sys.path:
            sys.path.append(cat_dir)
        import json
        try:
            import torch as torch_lib
            torch = torch_lib
            from utils import get_base_model
        except ImportError:
            print("WARNING: Torch or utils not found. Category prediction will be disabled.")
            self.category_model = None
            return
        except ImportError:
            print("Could not import get_base_model from utils")
            self.category_model = None
            return
        
        model_path = os.path.join(cat_dir, 'model.pt')
        class_map_path = os.path.join(cat_dir, 'class_indices.json')
        
        try:
            with open(class_map_path, 'r') as f:
                self.class_to_idx = json.load(f)
            self.idx_to_class = {v: k for k, v in self.class_to_idx.items()}
            
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            self.category_model = get_base_model(len(self.class_to_idx))
            self.category_model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.category_model = self.category_model.to(self.device)
            self.category_model.eval()
            print("PyTorch Category model loaded successfully.")
        except Exception as e:
            print(f"Failed to load PyTorch Category model: {e}")
            self.category_model = None

    def predict(self, img_path):
        print(f"DEBUG: Starting predict for {img_path}")
        if self.model is None:
            print("DEBUG: Binary model is None, cannot predict.")
            return None

        try:
            from tensorflow.keras.preprocessing import image
            from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

            print("DEBUG: Loading image...")
            img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
            img_array = image.img_to_array(img)
            img_array_expanded = np.expand_dims(img_array, axis=0)
            img_preprocessed = preprocess_input(img_array_expanded)

            print("DEBUG: Running binary prediction...")
            prediction = self.model.predict(img_preprocessed, verbose=0)[0][0]
            print(f"DEBUG: Binary prediction result: {prediction}")
            
            result = {
                "health_status": "Healthy",
                "confidence": float(prediction * 100),
                "risk_level": "Low",
                "prediction": "Healthy",
                "advice": "The plant appears healthy. Continue regular care and monitoring.",
                "disease": "Healthy",
                "description": "The plant appears healthy and shows no signs of disease.",
                "precautions": ["Continue regular care and monitoring", "Ensure proper watering and sunlight"],
                "treatment": ["No treatment required"]
            }

            if prediction < 0.5:
                print("DEBUG: Leaf predicted as Diseased.")
                result["health_status"] = "Diseased"
                result["prediction"] = "Diseased"
                result["confidence"] = float((1.0 - prediction) * 100)
                result["risk_level"] = "High" if result["confidence"] > 90 else "Medium"
                result["advice"] = "Isolate the plant immediately. Check for specific symptoms to identify the disease type. Consider applying appropriate fungicide or treatment."
                if self.category_model:
                    try:
                        import torch
                        from torchvision import transforms
                        from PIL import Image
                        
                        transform = transforms.Compose([
                            transforms.Resize(256),
                            transforms.CenterCrop(224),
                            transforms.ToTensor(),
                            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                        ])
                        img_pil = Image.open(img_path).convert('RGB')
                        input_tensor = transform(img_pil)
                        input_batch = input_tensor.unsqueeze(0).to(self.device)
                        
                        with torch.no_grad():
                            output = self.category_model(input_batch)
                            _, predicted_idx = torch.max(output, 1)
                            
                        predicted_class = self.idx_to_class[predicted_idx.item()]
                        result["disease_category"] = predicted_class
                        print(f"DEBUG: Category prediction: {predicted_class}")
                        
                        risk = result["confidence"]
                        import json
                        CATEGORY_MAP = {
                            "BACTERIAL   Orange Haunglongbing (Citrus_greening)": "bacterial/citrus_huanglongbing.json",
                            "BACTERIAL   Peach Bacterial spot": "bacterial/peach_bacterial_spot.json",
                            "BACTERIAL   Pepper bell Bacterial spot": "bacterial/pepper_bell_bacterial_spot.json",
                            "BACTERIAL   Tomato Bacterial spot": "bacterial/tomato_bacterial_spot.json",
                            "ENVIRONMENTAL   Potato": "environmental/potato_environmental_stress.json",
                            "ENVIRONMENTAL   Tomato": "environmental/tomato_environmental_stress.json",
                            "FUNGAL    Apple Apple scab": "fungal/apple_scab.json",
                            "FUNGAL    Apple Black rot": "fungal/apple_black_rot.json",
                            "FUNGAL    Apple Cedar apple rust": "fungal/apple_cedar_apple_rust.json",
                            "FUNGAL    Corn (maize) Common rust": "fungal/corn_common_rust.json",
                            "FUNGAL    Corn (maize) Northern Leaf Blight": "fungal/corn_northern_leaf_blight.json",
                            "FUNGAL    Grape Black rot": "fungal/grape_black_rot.json",
                            "FUNGAL    Grape Esca (Black_Measles)": "fungal/grape_esca_black_measles.json",
                            "FUNGAL    Grape Leaf blight (Isariopsis_Leaf_Spot)": "fungal/grape_leaf_blight.json",
                            "FUNGAL    Potato Early blight": "fungal/potato_early_blight.json",
                            "FUNGAL    Potato Late blight": "fungal/potato_late_blight.json",
                            "FUNGAL    Squash Powdery mildew": "fungal/squash_powdery_mildew.json",
                            "FUNGAL    Tomato Early blight": "fungal/tomato_early_blight.json",
                            "FUNGAL    Tomato Late blight": "fungal/tomato_late_blight.json",
                            "FUNGAL    Tomato Leaf Mold": "fungal/tomato_leaf_mold.json",
                            "FUNGAL    Tomato Target Spot": "fungal/tomato_target_spot.json",
                            "FUNGAL   Tomato Septoria leaf spot": "fungal/tomato_septoria_leaf_spot.json",
                            "FUNGAL  Corn (maize) Cercospora leaf spot Gray leaf spot": "fungal/corn_cercospora_leaf_spot.json",
                            "VIRAL   Tomato Yellow Leaf Curl Virus": "viral/tomato_yellow_leaf_curl_virus.json",
                            "VIRAL   Tomato mosaic virus": "viral/tomato_mosaic_virus.json"
                        }
                        kb_base_dir = os.path.join(os.path.dirname(Config.BASE_DIR), 'knowledge_base', 'knowledge_base')
                        mapped_json = CATEGORY_MAP.get(predicted_class)
                        
                        print(f"DEBUG: Predicted category label: '{predicted_class}'")
                        print(f"DEBUG: Matched mapped_json: {mapped_json}")
                        
                        if mapped_json:
                            json_path = os.path.join(kb_base_dir, mapped_json)
                            if os.path.exists(json_path):
                                with open(json_path, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                    
                                    severity = data.get("severity_level", "Unknown")
                                    
                                    data["is_critical"] = (risk >= 90)
                                    result["knowledge_base"] = data
                                    
                                    # Format for frontend response
                                    result["disease"] = data.get("disease_name", predicted_class)
                                    result["description"] = data.get("short_description", "No additional information available")
                                    
                                    # Extract precautions
                                    precautions_data = data.get("precautions", {})
                                    prec_list = []
                                    if isinstance(precautions_data, dict):
                                        prec_list = list(precautions_data.values())
                                    elif isinstance(precautions_data, list):
                                        prec_list = precautions_data
                                    result["precautions"] = prec_list if prec_list else ["No specific precautions available."]
                                    
                                    # Extract treatments
                                    treatment_data = data.get("treatment", {})
                                    treat_list = []
                                    if isinstance(treatment_data, dict):
                                        if "step_by_step" in treatment_data and isinstance(treatment_data["step_by_step"], list):
                                            treat_list = treatment_data["step_by_step"]
                                        else:
                                            # Gather all text values from treatment dict
                                            for k, v in treatment_data.items():
                                                if isinstance(v, list) and k != "suggested_fungicides":
                                                    treat_list.extend([str(item) for item in v])
                                                elif isinstance(v, str):
                                                    treat_list.append(v)
                                    elif isinstance(treatment_data, list):
                                        treat_list = treatment_data
                                    
                                    if risk >= 90:
                                        treat_list.insert(0, "⚠️ This plant is not suitable to keep. There is no solution to cure it at this stage. Please remove and destroy this plant immediately.")
                                        
                                    result["treatment"] = treat_list if treat_list else ["No specific treatments available."]
                                    print(f"DEBUG: Successfully loaded knowledge base for {predicted_class}")

                            else:
                                print(f"DEBUG: Knowledge base file NOT FOUND at {json_path}")
                                result["knowledge_base"] = f"⚠️ [Warning: Knowledge base file {mapped_json} not found]"
                                result["disease"] = predicted_class
                                result["description"] = "No additional information available"
                                result["precautions"] = []
                                result["treatment"] = []
                        else:
                            print(f"DEBUG: Unmapped category '{predicted_class}'")
                            result["knowledge_base"] = f"⚠️ [Warning: Unmapped category {predicted_class}]"
                            result["disease"] = predicted_class
                            result["description"] = "No additional information available"
                            result["precautions"] = []
                            result["treatment"] = []

                    except Exception as e:
                        print(f"DEBUG: Error calculating PyTorch category: {e}")

            print("DEBUG: Prediction complete.")
            return result
            
        except Exception as e:
            import traceback
            print(f"DEBUG: Error during prediction: {e}")
            traceback.print_exc()
            return None

# Singleton instance
ai_engine = AIEngine()
