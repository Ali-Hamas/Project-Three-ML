#!/usr/bin/env python3
"""
FastAPI server for NER extraction.
Serves the fine-tuned Qwen2.5-0.5B model with LoRA adapters.
"""
import os
import json
import time
from pathlib import Path
from typing import Optional
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Configure M drive paths
MODEL_DIR = r"M:\MCHINE LERNING\Project one\models"
FINE_TUNED_MODEL_DIR = r"M:\MCHINE LERNING\Project one\models\fine_tuned"

os.environ["HF_HOME"] = MODEL_DIR
os.environ["TRANSFORMERS_CACHE"] = os.path.join(MODEL_DIR, "transformers")

# FastAPI app
app = FastAPI(
    title="NER Extraction API",
    description="Extract named entities using fine-tuned Qwen2.5-0.5B",
    version="1.0.0"
)

# Request/Response models
class ExtractionRequest(BaseModel):
    text: str
    max_length: Optional[int] = 512

class EntityExtraction(BaseModel):
    names: list
    organizations: list
    locations: list

class ExtractionResponse(BaseModel):
    success: bool
    entities: Optional[EntityExtraction] = None
    inference_time_ms: float
    error: Optional[str] = None

# Global variables for model
model = None
tokenizer = None
device = "cuda" if torch.cuda.is_available() else "cpu"

@app.on_event("startup")
async def load_model():
    """Load model on startup"""
    global model, tokenizer
    print(f"⏳ Loading model on device: {device}")

    try:
        # Load base model
        tokenizer = AutoTokenizer.from_pretrained(
            "Qwen/Qwen2.5-1.5B-Instruct",
            trust_remote_code=True,
            cache_dir=os.path.join(MODEL_DIR, "transformers")
        )

        model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen2.5-1.5B-Instruct",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map=device,
            trust_remote_code=True,
            cache_dir=os.path.join(MODEL_DIR, "transformers")
        )

        # Load LoRA adapters if fine-tuned model exists
        if Path(FINE_TUNED_MODEL_DIR).exists():
            print(f"⏳ Loading LoRA adapters from {FINE_TUNED_MODEL_DIR}")
            model = PeftModel.from_pretrained(model, FINE_TUNED_MODEL_DIR)
            model = model.merge_and_unload()
            print(f"✅ LoRA adapters merged")

        model.eval()
        print(f"✅ Model loaded successfully on {device}")

    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": device
    }

@app.post("/extract", response_model=ExtractionResponse)
async def extract_entities(request: ExtractionRequest) -> ExtractionResponse:
    """
    Extract named entities from text

    Args:
        text: Input text to extract entities from
        max_length: Maximum output length (default: 512)

    Returns:
        ExtractionResponse with extracted entities
    """
    if not model or not tokenizer:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        start_time = time.time()

        # Create prompt
        prompt = f"""Extract named entities from the text.

Text: {request.text}

Extract and categorize:
- Names (people)
- Organizations
- Locations

Output as JSON with keys: names, organizations, locations"""

        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt").to(device)

        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=request.max_length,
                num_beams=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=False
            )

        # Decode
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                entities_dict = json.loads(json_str)
            else:
                # Fallback: empty extraction
                entities_dict = {
                    "names": [],
                    "organizations": [],
                    "locations": []
                }
        except json.JSONDecodeError:
            entities_dict = {
                "names": [],
                "organizations": [],
                "locations": []
            }

        inference_time = (time.time() - start_time) * 1000

        return ExtractionResponse(
            success=True,
            entities=EntityExtraction(**entities_dict),
            inference_time_ms=inference_time
        )

    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return ExtractionResponse(
            success=False,
            inference_time_ms=0,
            error=str(e)
        )

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "NER Extraction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "extract": "/extract (POST)",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting API server on http://localhost:8000")
    print(f"📚 Docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
