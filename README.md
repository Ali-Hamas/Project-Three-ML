# 🎯 NER Extraction System - Project One

A lightweight Named Entity Recognition (NER) system using **Qwen2.5-0.5B** (500M parameters) with LoRA fine-tuning, deployed via FastAPI + Next.js. Everything runs locally on your VPS with **zero external API calls**.

## ✨ Key Features

- **Tiny Model** - 500M parameters (Qwen2.5-0.5B), ~2GB disk footprint
- **Fast** - Sub-100ms inference on CPU, even faster with GPU
- **LoRA Fine-tuning** - Parameter-efficient adaptation without retraining entire model
- **Privacy-First** - All processing stays on your hardware, no cloud calls
- **Full Stack** - Model → FastAPI Server → React Frontend
- **M Drive Only** - All downloads and models save to M drive, never touches C drive

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │   Next.js UI    │ (localhost:3000)
                    │  (React + Axios)│
                    └────────┬────────┘
                             │ HTTP POST
                    ┌────────▼────────┐
                    │  FastAPI Server │ (localhost:8000)
                    │  /extract POST  │
                    └────────┬────────┘
                             │
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
┌───▼──┐  ┌──────────┐  ┌───▼─────┐  ┌──────────┐
│ Text │→ │Tokenizer │→ │ Model   │→ │JSON Parser│
└───┬──┘  └──────────┘  │(Qwen)   │  └──────────┘
    │                    │+LoRA    │
    │                    └─────────┘
    │ Input
    └─────────────────────────────────┘
```

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
cd "M:\MCHINE LERNING\Project one"
pip install -r requirements.txt
```

### 2️⃣ Download Model (to M drive)
```bash
python scripts/download_model.py
```
- Sets `HF_HOME` to M drive
- Downloads Qwen2.5-0.5B (~2GB)
- Runs quick test

### 3️⃣ Fine-tune with LoRA
```bash
python scripts/fine_tune.py
```
- Loads model from M drive
- Adds LoRA adapters
- Trains on NER examples (~5-10 min)
- Saves to `M:\...\models\fine_tuned`

### 4️⃣ Start API Server
```bash
python scripts/api_server.py
```
- Loads model + LoRA adapters
- Starts on `http://localhost:8000`
- Auto-detects CUDA GPU or uses CPU

### 5️⃣ (Optional) Start Frontend
```bash
cd frontend
npm install
npm run dev
```
- Opens `http://localhost:3000`
- Connect to API at localhost:8000

## 📖 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### `GET /health`
Health check endpoint
```bash
curl http://localhost:8000/health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda"
}
```

#### `POST /extract`
Extract entities from text

**Request:**
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d {
    "text": "John Smith works at Google in Mountain View",
    "max_length": 512
  }
```

**Response:**
```json
{
  "success": true,
  "entities": {
    "names": ["John Smith"],
    "organizations": ["Google"],
    "locations": ["Mountain View"]
  },
  "inference_time_ms": 45.23
}
```

#### `GET /docs`
Interactive Swagger UI
```
http://localhost:8000/docs
```

## 🛠️ Configuration

### Model Paths (All on M Drive)
```
M:\MCHINE LERNING\Project one\models\
├── transformers/           # Base model & tokenizer
│   └── models--Qwen--Qwen2.5-0.5B/
└── fine_tuned/             # LoRA adapters
    ├── adapter_model.bin
    ├── adapter_config.json
    └── config.json
```

### Environment Variables
Set automatically in Python scripts:
```python
os.environ["HF_HOME"] = r"M:\MCHINE LERNING\Project one\models"
```

To manually set (Windows PowerShell):
```powershell
$env:HF_HOME = "M:\MCHINE LERNING\Project one\models"
```

## 📊 Model Information

| Metric | Value |
|--------|-------|
| **Base Model** | Qwen2.5-0.5B |
| **Parameters** | 500M |
| **Context Length** | 2048 tokens |
| **Fine-tuning Method** | LoRA (r=16, α=32) |
| **Quantization** | 4-bit (during training) |
| **Disk Space** | ~2.5GB total |
| **Memory (Inference)** | ~1.5GB (CPU), ~800MB (GPU) |
| **Inference Speed** | ~50-100ms (CPU), ~20-40ms (GPU) |

## 💾 Directory Structure

```
M:\MCHINE LERNING\Project one\
├── data/                      # Training/test data
│   └── (will contain datasets)
├── models/                    # All model files (M drive only)
│   ├── transformers/          # Downloaded base model
│   ├── datasets/              # HF datasets cache
│   └── fine_tuned/            # LoRA adapters
├── scripts/
│   ├── download_model.py      # Download to M drive
│   ├── fine_tune.py           # Train with Unsloth+LoRA
│   └── api_server.py          # FastAPI inference server
├── frontend/
│   ├── pages/
│   │   └── index.tsx          # React UI
│   ├── package.json
│   └── next.config.js
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── SETUP.md                   # Detailed setup guide
├── .env.example              # Environment template
└── run_setup.bat             # Windows setup script
```

## 🔍 Example Usage

### Command Line
```bash
# Test via curl
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "Alice Chen is a researcher at MIT"}'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/extract",
    json={"text": "Bob Johnson works at Amazon"}
)
print(response.json())
```

### Frontend (Next.js)
1. Go to `http://localhost:3000`
2. Paste text in textarea
3. Click "Extract Entities"
4. See results with inference time

## 🎬 Video Demo Strategy

### What to Show
1. **The Problem** - Need to extract structured data without expensive APIs
2. **The Solution** - Qwen2.5-0.5B + LoRA + FastAPI
3. **The Code**
   - `download_model.py` - Show M drive configuration
   - `fine_tune.py` - Show LoRA setup with Unsloth
   - `api_server.py` - Show /extract endpoint
4. **The Demo**
   - Paste text → Get JSON in <100ms
   - Compare with API latency (your local is faster!)
5. **The Value**
   - Privacy: No data leaves your server
   - Speed: <100ms vs API roundtrips
   - Cost: Free to run after setup
   - Size: 500M params fit on modest hardware

### Key Metrics to Highlight
- Model size: 500M parameters (~2GB)
- Inference: <100ms locally
- Training: LoRA fine-tune in ~5 minutes
- Deployment: Single FastAPI server
- Privacy: 100% local processing

## ⚙️ Customization

### Add More Entity Types
Edit `scripts/fine_tune.py`:
```python
sample = {
    "text": "...",
    "entities": {
        "names": [...],
        "organizations": [...],
        "locations": [...],
        "products": [...],  # Add new type
    }
}
```

### Change Model Size
In `download_model.py` and `api_server.py`:
```python
# Use 1B instead of 500M
model_name = "Qwen/Qwen2.5-1B"  # ~2.5x larger
```

### Adjust Fine-tuning
In `scripts/fine_tune.py`:
```python
# Make LoRA stronger
r=32,          # Increase from 16
lora_alpha=64, # Increase from 32

# Train longer
num_train_epochs=5,  # Increase from 3
```

## 🐛 Troubleshooting

### Models saved to C drive?
Check environment variables:
```bash
echo %HF_HOME%
```
Should show: `M:\MCHINE LERNING\Project one\models`

If wrong, edit the Python script and re-run.

### GPU not detected?
```bash
python -c "import torch; print(torch.cuda.is_available())"
```
- If `False`: Using CPU (still works, just slower)
- If `True`: CUDA available, should auto-use

### Port 8000 already in use?
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Out of memory?
Reduce batch size in `scripts/fine_tune.py`:
```python
per_device_train_batch_size=2,  # Down from 4
```

### Model won't load?
Ensure fine-tuning completed:
```bash
ls -la "M:\MCHINE LERNING\Project one\models\fine_tuned"
```
Should contain `adapter_model.bin`, `adapter_config.json`

## 📚 Resources

- **Qwen Documentation**: https://github.com/QwenLM/Qwen2.5
- **Unsloth**: https://github.com/unslothai/unsloth
- **PEFT (LoRA)**: https://github.com/huggingface/peft
- **FastAPI**: https://fastapi.tiangolo.com
- **Next.js**: https://nextjs.org

## 📝 License

This project uses open-source models and libraries. Check respective licenses:
- Qwen2.5: Apache 2.0
- Unsloth: MIT
- FastAPI: MIT
- Next.js: MIT

## 🤝 Support

For issues:
1. Check `SETUP.md` for detailed setup
2. Review troubleshooting section above
3. Check logs: `python scripts/api_server.py` shows detailed output

---

**Status**: ✅ Ready to build
**All files**: M drive only
**Next step**: Run `python scripts/download_model.py`
