import sys
import os
sys.path.append(os.path.abspath(r'C:\Users\tejas\OneDrive\Desktop\TEJU (2)\TEJU\model-main2\AgroCareAI\backend'))
from ai_engine import ai_engine

if ai_engine.model:
    print("TF Model OK")
else:
    print("TF Model False")

if ai_engine.category_model:
    print("PT Model OK")
else:
    print("PT Model False")
