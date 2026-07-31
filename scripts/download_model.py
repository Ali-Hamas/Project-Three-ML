#!/usr/bin/env python3
"""
Download Qwen2.5-0.5B model to M drive.
This script configures Hugging Face to save models on the M drive.
"""
import os
import sys
from pathlib import Path

# Set Hugging Face cache to M drive
MODEL_DIR = r"M:\MCHINE LERNING\Project one\models"
os.environ["HF_HOME"] = MODEL_DIR
os.environ["TRANSFORMERS_CACHE"] = os.path.join(MODEL_DIR, "transformers")
os.environ["HF_DATASETS_CACHE"] = os.path.join(MODEL_DIR, "datasets")

Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print(f"📥 Setting HF_HOME to: {MODEL_DIR}")
print(f"🔄 Downloading Qwen2.5-0.5B model...")

model_name = "Qwen/Qwen2.5-1.5B-Instruct"

try:
    # Load tokenizer from cache (already installed)
    print(f"⏳ Loading tokenizer from cache...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        cache_dir=os.path.join(MODEL_DIR, "transformers")
    )
    print(f"✅ Tokenizer loaded")

    # Load model from cache (already installed)
    print(f"⏳ Loading model from cache...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="cpu",
        trust_remote_code=True,
        cache_dir=os.path.join(MODEL_DIR, "transformers")
    )
    print(f"✅ Model loaded successfully!")

    print(f"\n📊 Model Info:")
    print(f"   - Model: {model_name}")
    print(f"   - Parameters: ~1.5B (3x better than 0.5B)")
    print(f"   - Location: {os.path.join(MODEL_DIR, 'transformers')}")
    print(f"   - Device: CPU (ready for inference)")

    # Quick test
    print(f"\n🧪 Quick inference test...")
    inputs = tokenizer("Extract: John works at Google", return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=50)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"   Test output: {result[:80]}...")
    print(f"✅ Model working correctly!")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
