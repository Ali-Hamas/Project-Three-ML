# NER Extraction Project - Setup Guide

## 📁 Project Structure
```
M:\MCHINE LERNING\Project one\
├── data/                 # Training data (will be created)
├── models/               # Downloaded models and fine-tuned adapters
├── scripts/              # Python scripts
│   ├── download_model.py    # Download Qwen2.5-0.5B to M drive
│   ├── fine_tune.py         # Fine-tune with Unsloth + LoRA
│   └── api_server.py        # FastAPI server
├── frontend/             # Next.js UI
│   ├── pages/
│   │   └── index.tsx     # Main extraction interface
│   └── package.json
├── requirements.txt      # Python dependencies
└── SETUP.md             # This file
```

## 🚀 Quick Start

### Step 1: Install Python Dependencies
```bash
cd M:\MCHINE LERNING\Project one
pip install -r requirements.txt
```

### Step 2: Download Model to M Drive
```bash
python scripts/download_model.py
```
**What this does:**
- Sets `HF_HOME` environment variable to `M:\MCHINE LERNING\Project one\models`
- Downloads Qwen2.5-0.5B tokenizer and model (will use ~2GB space on M drive)
- Tests the model with a quick inference
- **All files stay on M drive, not C drive**

### Step 3: Fine-tune with LoRA
```bash
python scripts/fine_tune.py
```
**What this does:**
- Loads the base model from M drive
- Adds LoRA adapters (Low-Rank Adaptation)
- Fine-tunes on sample NER data (~5-10 minutes)
- Saves adapters to `M:\MCHINE LERNING\Project one\models\fine_tuned`

### Step 4: Start FastAPI Server
```bash
python scripts/api_server.py
```
Server runs on `http://localhost:8000`

**Endpoints:**
- `GET /` - API info
- `GET /health` - Health check
- `POST /extract` - Extract entities from text
- `GET /docs` - Interactive API documentation (Swagger UI)

### Step 5: Setup Frontend (Optional)
```bash
cd M:\MCHINE LERNING\Project one\frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`

## 🔧 Configuration

### Model Paths (All on M Drive)
```
M:\MCHINE LERNING\Project one\models\
├── transformers/        # Downloaded base model
└── fine_tuned/          # LoRA adapters
```

Environment variables are set automatically in Python scripts:
```python
os.environ["HF_HOME"] = r"M:\MCHINE LERNING\Project one\models"
```

### API Configuration
- Host: `0.0.0.0` (accessible locally)
- Port: `8000`
- Device: Auto-detects CUDA GPU, falls back to CPU

## 📊 Testing

### Quick API Test
```bash
# Terminal 1: Start API server
python scripts/api_server.py

# Terminal 2: Test extraction
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "John Smith works at Google in Mountain View"}'
```

### Frontend Test
1. Start API server (Terminal 1)
2. Start frontend dev server (Terminal 2)
3. Open `http://localhost:3000` in browser
4. Paste text and click "Extract Entities"

## 💾 Disk Space Requirements
- Base model (~2GB): Downloaded once
- LoRA adapters (~50MB): Created during fine-tuning
- Dependencies: ~500MB
- **Total: ~2.5GB on M drive**

## 🐛 Troubleshooting

### Models saving to C drive?
Ensure Python scripts use the `HF_HOME` environment variable:
```bash
# Check where models are downloading
echo %HF_HOME%
# Should output: M:\MCHINE LERNING\Project one\models
```

### Out of memory during fine-tuning?
The scripts use:
- `load_in_4bit=True` (quantization)
- Batch size: 4
- Gradient accumulation: 2
These are already optimized for 2-4GB VRAM.

### API server won't start?
Check if port 8000 is in use:
```bash
netstat -ano | findstr :8000
# Kill process if needed:
taskkill /PID <PID> /F
```

### Frontend won't connect to API?
Ensure API server is running, then check:
```bash
# Test API health
curl http://localhost:8000/health
```

## 📚 Next Steps

1. **Expand training data** - Add more NER examples in `scripts/fine_tune.py`
2. **Customize extraction schema** - Modify entity types (Person, Org, Location, etc.)
3. **Deploy on VPS** - Use Docker to containerize the API
4. **Add more features** - Confidence scores, entity linking, batch processing

## 🎯 Video Demonstration Talking Points

1. **Speed** - Show inference times (<100ms for most texts)
2. **Privacy** - Data never leaves your VPS, no API calls to OpenAI
3. **Size** - 500M parameters = <3GB disk, runs on modest hardware
4. **Fine-tuning** - Custom LoRA adapters for your specific domain
5. **Architecture** - Full stack: Model → API → UI, all deployable together

