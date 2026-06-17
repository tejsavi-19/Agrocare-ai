import os
import sys
import json
import traceback
from PIL import Image

# ---------------------------------------------------------
# PATH CONFIGURATION
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_1_PATH = os.path.join(BASE_DIR, 'models', 'leaf_stem_healthy_diseased.keras')

# Teju/cat paths
CAT_DIR = r"c:\Users\USER\Downloads\TEJU\cat"
MODEL_2_PATH = os.path.join(CAT_DIR, 'model.pt')
CLASS_MAP_PATH = os.path.join(CAT_DIR, 'class_indices.json')

if CAT_DIR not in sys.path:
    sys.path.append(CAT_DIR)

# ---------------------------------------------------------
# GLOBAL MODELS
# ---------------------------------------------------------
_binary_model = None
_category_model = None
_class_to_idx = None
_idx_to_class = None
_device = None

def load_health_model():
    """Load the Keras binary classification model."""
    global _binary_model
    if _binary_model is None:
        import tensorflow as tf
        from tensorflow import keras
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TF logs
        if not os.path.exists(MODEL_1_PATH):
            raise FileNotFoundError(f"Binary model not found at {MODEL_1_PATH}")
        _binary_model = keras.models.load_model(MODEL_1_PATH, compile=False)
    return _binary_model

def load_category_model():
    """Load the PyTorch categorical classification model."""
    global _category_model, _class_to_idx, _idx_to_class, _device
    if _category_model is None:
        import torch
        from utils import get_base_model
        
        if not os.path.exists(MODEL_2_PATH) or not os.path.exists(CLASS_MAP_PATH):
            raise FileNotFoundError(f"Category model files missing in {CAT_DIR}")
        
        with open(CLASS_MAP_PATH, 'r') as f:
            _class_to_idx = json.load(f)
            
        _idx_to_class = {v: k for k, v in _class_to_idx.items()}
        num_classes = len(_class_to_idx)
        
        _device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        _category_model = get_base_model(num_classes)
        _category_model.load_state_dict(torch.load(MODEL_2_PATH, map_location=_device))
        _category_model = _category_model.to(_device)
        _category_model.eval()
        
    return _category_model

def predict_health(image_path):
    """
    Predict Healthy vs Diseased using Model 1 (Keras).
    """
    import numpy as np
    
    # Load model
    model = load_health_model()
    
    # Preprocess image
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        raise ValueError(f"Failed to load image for health prediction: {e}")

    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    pred_output = model.predict(img_array, verbose=0)
    prediction = float(pred_output.flatten()[0])
    
    if prediction > 0.5:
        status = "Diseased"
        risk = prediction * 100
    else:
        status = "Healthy"
        risk = (1.0 - prediction) * 100
    
    return status, risk

def predict_category(image_path):
    """
    Predict the disease category using Model 2 (PyTorch).
    """
    import torch
    from torchvision import transforms
    
    # Load model and dependencies
    model = load_category_model()
    
    # Preprocess image
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        raise ValueError(f"Failed to load image for category prediction: {e}")
        
    input_tensor = transform(img)
    input_batch = input_tensor.unsqueeze(0).to(_device)
    
    # Predict
    with torch.no_grad():
        output = model(input_batch)
        _, predicted_idx = torch.max(output, 1)
        predicted_idx = predicted_idx.item()
        
    predicted_class = _idx_to_class[predicted_idx]
    return predicted_class

def run_pipeline(image_path):
    """
    Runs the full integrated pipeline with robust error logging.
    """
    
    if not os.path.exists(image_path):
        print(f"ERROR: Image not found at {image_path}", file=sys.stderr)
        return
        
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

    try:
        # Step 1: Binary classification
        status, risk = predict_health(image_path)
        
        if status.strip().lower() == "diseased":
            try:
                category = predict_category(image_path)
                print(f"Diseased - {category}")
                
                # Check critical risk level
                if risk >= 90:
                    print("\n⚠️ This disease is at a critical stage.")
                    print("No treatment can cure it. It is better to remove or isolate the plant to prevent spreading.")
                else:
                    # Treatable, print exact JSON content
                    kb_base_dir = r"c:\Users\USER\Downloads\TEJU\knowledge_base\knowledge_base"
                    mapped_json = CATEGORY_MAP.get(category)
                    
                    if mapped_json:
                        json_path = os.path.join(kb_base_dir, mapped_json)
                        if os.path.exists(json_path):
                            print("\n", end="")
                            with open(json_path, 'r', encoding='utf-8') as f:
                                import json
                                data = json.load(f)
                                
                                severity = data.get("severity_level", "Unknown")
                                spread = data.get("spread_risk", "Unknown")
                                category_text = data.get("disease_category", "")
                                no_cure = "viral" in category_text.lower() or "virus" in category_text.lower()
                                
                                report = [
                                    f"🌿 Disease Report",
                                    f"🦠 Disease Name\n{data.get('disease_name', 'Unknown')}\n",
                                    f"📂 Category\n{category_text}\n",
                                    f"🌱 Affected Plant\n{data.get('affected_plant', 'Unknown')}\n",
                                    f"📝 Description\n{data.get('short_description', '')}\n",
                                    f"🔍 What is it?\n{data.get('detailed_explanation', {}).get('what_is_it', '')}\n",
                                    f"⚠️ Symptoms",
                                    f"Leaves:\n{data.get('symptoms', {}).get('leaf_symptoms', '')}",
                                    f"Stem:\n{data.get('symptoms', {}).get('stem_symptoms', '')}",
                                    f"Fruit:\n{data.get('symptoms', {}).get('fruit_symptoms', '')}\n",
                                    f"🧬 Causes\n{data.get('causes', {}).get('biological_or_environmental', '')}\n",
                                    f"🚨 Risk Level\n{severity} (Spread: {spread})\n",
                                    f"🛡️ Prevention Tips",
                                    f"• {data.get('precautions', {}).get('steps_to_prevent', '')}",
                                    f"• {data.get('precautions', {}).get('crop_rotation', '')}",
                                    f"• {data.get('precautions', {}).get('hygiene', '')}",
                                    f"• {data.get('precautions', {}).get('soil_care', '')}\n",
                                    f"💊 Treatment"
                                ]
                                
                                if severity == "High" and no_cure:
                                    report.extend([
                                        "❌ No Cure Available",
                                        "No organic treatment",
                                        "No chemical treatment\n",
                                        "🚫 Recommended Action",
                                        "⚠️ This disease cannot be cured.",
                                        "It is strongly advised to remove and destroy the plant to prevent spread.\n"
                                    ])
                                else:
                                    report.extend([
                                        f"🟢 Organic: {data.get('treatment', {}).get('organic', '')}",
                                        f"🧪 Chemical: {data.get('treatment', {}).get('chemical', '')}",
                                        f"✅ Step-by-Step:"
                                    ])
                                    # Add steps
                                    for step in data.get('treatment', {}).get('step_by_step', []):
                                        report.append(step)
                                    report.append("") # spacer

                                report.extend([
                                    f"🧑‍🌾 Farmer Tip",
                                    f"{data.get('additional_farmer_tips', '')}"
                                ])
                                
                                print("\n" + "\n".join(report))
                        else:
                            print(f"\n[Warning: Knowledge base file {mapped_json} not found]")
                    else:
                        print(f"\n[Warning: Unmapped category {category}]")
                        
            except Exception as e:
                print(f"Diseased - [Category Error: {e}]")
        else:
            print("Healthy")
            
    except Exception as e:
        print("\n--- PIPELINE EXECUTION ERROR ---", file=sys.stderr)
        print(f"Error Details: {str(e)}", file=sys.stderr)
        print("Stack Trace:", file=sys.stderr)
        traceback.print_exc()
        print("-------------------------------", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python integrated_pipeline.py <path_to_image>")
        sys.exit(1)
        
    target_image = sys.argv[1]
    run_pipeline(target_image)
