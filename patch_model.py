import zipfile
import json
import os
import shutil

model_path = r"C:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\models\leaf_stem_healthy_diseased.keras"
temp_dir = "temp_keras_patch"
patched_model_path = r"C:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\models\leaf_stem_healthy_diseased_patched.keras"

print("Extracting...")
with zipfile.ZipFile(model_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

config_path = os.path.join(temp_dir, "config.json")
print("Reading config.json...")
with open(config_path, "r", encoding="utf-8") as f:
    config_data = json.load(f)

def clean_config(data):
    if isinstance(data, dict):
        # Remove quantization_config if it exists
        if "quantization_config" in data:
            del data["quantization_config"]
        for k, v in data.items():
            clean_config(v)
    elif isinstance(data, list):
        for item in data:
            clean_config(item)

print("Patching config.json...")
clean_config(config_data)

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=2)

print("Repacking into patched .keras...")
# Change directory so zip file doesn't have parent folder structure
os.chdir(temp_dir)
with zipfile.ZipFile(patched_model_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("."):
        for file in files:
            zipf.write(os.path.join(root, file))

os.chdir("..")
shutil.rmtree(temp_dir)
print(f"Done! Patched model saved to: {patched_model_path}")
