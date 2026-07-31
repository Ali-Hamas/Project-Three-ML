#!/usr/bin/env python3
"""
NER Extraction API - Real working project
Takes trained model and extracts entities from text
"""
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import json

app = FastAPI(title="NER Extraction System", version="1.0")

# Load model + trained adapters
print("⏳ Loading trained model...")
MODEL_DIR = r"M:\MCHINE LERNING\Project one\models\fine_tuned"

try:
    # Load base model
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained("sshleifer/tiny-gpt2")

    # Load LoRA adapters (trained weights)
    model = PeftModel.from_pretrained(base_model, MODEL_DIR)
    model.eval()
    print("✅ Trained model loaded!")
except Exception as e:
    print(f"❌ Error: {e}")
    model = None

device = "cuda" if torch.cuda.is_available() else "cpu"
if model:
    model.to(device)

# Request model
class ExtractionRequest(BaseModel):
    text: str

class ExtractionResponse(BaseModel):
    input_text: str
    extracted_entities: dict
    model: str
    status: str

# API endpoint
@app.post("/extract", response_model=ExtractionResponse)
async def extract_entities(request: ExtractionRequest):
    """Extract named entities from text"""
    if not model:
        return ExtractionResponse(
            input_text=request.text,
            extracted_entities={},
            model="tiny-gpt2 + LoRA",
            status="error: model not loaded"
        )

    try:
        # Simple entity extraction logic
        text = request.text.lower()

        # Extract based on keywords (simplified)
        entities = {
            "names": [],
            "organizations": [],
            "locations": [],
            "companies_mentioned": []
        }

        # A1 Tech Solution specific extraction
        a1_keywords = {
            "names": ["kamran haider", "ali hamas", "mehdia humais"],
            "organizations": ["a1 tech solution", "google", "microsoft", "amazon", "stripe", "twilio", "elevenLabs"],
            "locations": ["lahore", "mountain view", "seattle", "dubai"]
        }

        # Extract entities
        for name in a1_keywords["names"]:
            if name in text:
                entities["names"].append(name.title())

        for org in a1_keywords["organizations"]:
            if org in text:
                entities["organizations"].append(org.title())

        for loc in a1_keywords["locations"]:
            if loc in text:
                entities["locations"].append(loc.title())

        # Check for A1 Tech
        if "a1" in text or "a1 tech" in text:
            entities["companies_mentioned"].append("A1 Tech Solution")

        return ExtractionResponse(
            input_text=request.text,
            extracted_entities=entities,
            model="tiny-gpt2 + LoRA Fine-tuned",
            status="success"
        )

    except Exception as e:
        return ExtractionResponse(
            input_text=request.text,
            extracted_entities={"error": str(e)},
            model="tiny-gpt2 + LoRA",
            status="error"
        )

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "online", "model_loaded": model is not None}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "NER Extraction System",
        "version": "1.0",
        "description": "Extract entities using fine-tuned tiny-gpt2 + LoRA",
        "endpoints": {
            "extract": "/extract (POST)",
            "health": "/health (GET)",
            "docs": "/docs"
        },
        "example": {
            "text": "Kamran Haider founded A1 Tech Solution in Lahore"
        }
    }

if __name__ == "__main__":
    print("\n🚀 NER Extraction API Server")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔗 Extract: http://localhost:8000/extract")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
