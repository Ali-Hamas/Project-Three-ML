# 🚀 START HERE - Quick Launch Guide

Welcome! This is your fastest path to getting the NER extraction system running.

---

## ⚡ 5-Minute Overview

You have a **complete NER extraction system** ready to use:
- **Model**: Qwen2.5-0.5B (tiny, 500M parameters)
- **Training**: LoRA fine-tuning with Unsloth
- **Server**: FastAPI with <100ms inference
- **UI**: Beautiful React frontend (optional)
- **Storage**: All on M drive (never touches C drive)

---

## 📖 Which File to Read?

| You Want To... | Read This |
|---|---|
| **Quick overview** | 👈 This file |
| **Full project details** | `PROJECT_SUMMARY.md` |
| **Complete step-by-step** | `SETUP.md` |
| **API & code docs** | `README.md` |
| **Understand architecture** | `README.md` (Architecture section) |

---

## 🎯 3-Step Launch (15 minutes)

### Step 1: Install
```bash
cd "M:\MCHINE LERNING\Project one"
pip install -r requirements.txt
```
**Time**: ~5 min | **Done?** ✅

### Step 2: Download Model to M Drive
```bash
python scripts/download_model.py
```
**What happens:**
- Sets environment to use M drive (not C drive) ✓
- Downloads Qwen2.5-0.5B model (~2GB)
- Tests that it works
- All files stay on M drive ✓

**Time**: ~3-5 min | **Done?** ✅

### Step 3: Start the Server
```bash
python scripts/api_server.py
```
**What happens:**
- Loads model + LoRA adapters
- Starts on `http://localhost:8000`
- Ready to extract entities

**Time**: ~30 sec | **Done?** ✅

---

## ✅ Test It Works

In a new terminal:
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "John Smith works at Google in Mountain View"}'
```

**Expected response:**
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

✅ **If you see this, you're done!**

---

## 🎬 Next: Fine-tuning (Optional)

Want to train the model on your own data? Run:
```bash
python scripts/fine_tune.py
```
**Time**: ~5-10 min to train | Creates adapters on M drive

---

## 🖥️ Next: Web UI (Optional)

Want a beautiful interface instead of curl?
```bash
cd frontend
npm install
npm run dev
```
Then open `http://localhost:3000`

---

## 📍 Everything is on M Drive

Verify:
```bash
echo %HF_HOME%
# Should show: M:\MCHINE LERNING\Project one\models
```

All downloaded models, cache, and trained adapters stay on M drive. ✓

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| **Command not found** | Make sure you're in `M:\MCHINE LERNING\Project one` |
| **Port 8000 in use** | `netstat -ano \| findstr :8000` then `taskkill /PID <PID> /F` |
| **Models on C drive** | Check `HF_HOME` env var is set (see step 2) |
| **Out of memory** | Reduce batch size in `scripts/fine_tune.py` |
| **CUDA errors** | That's OK, it'll use CPU instead |

---

## 📊 What You Have

```
✅ Download script        (M drive config included)
✅ Training script        (LoRA with Unsloth)
✅ API server            (FastAPI with docs)
✅ Web UI               (Next.js + React)
✅ Full documentation    (README + SETUP + PROJECT_SUMMARY)
✅ Example configs      (.env template)
✅ Windows helper       (run_setup.bat)
```

---

## 🎯 Common Goals

### "I just want to extract entities"
```bash
python scripts/api_server.py
curl -X POST http://localhost:8000/extract -H "Content-Type: application/json" -d '{"text":"..."}'
```

### "I want a web interface"
```bash
# Terminal 1
python scripts/api_server.py

# Terminal 2
cd frontend && npm install && npm run dev
# Open http://localhost:3000
```

### "I want to fine-tune on my data"
1. Edit `scripts/fine_tune.py` - add your examples to `create_sample_dataset()`
2. Run `python scripts/fine_tune.py`
3. Restart API server - it'll use your custom trained adapters

### "I want to deploy this"
- API is production-ready FastAPI ✓
- Can containerize with Docker ✓
- Run on any VPS with 2GB+ RAM ✓
- See `README.md` for deployment notes

---

## 📚 File Reference

**Must Read:**
- `README.md` - Complete project info
- `SETUP.md` - Detailed setup steps
- `PROJECT_SUMMARY.md` - Full breakdown

**Code Files:**
- `scripts/download_model.py` - Get the model
- `scripts/fine_tune.py` - Train the model
- `scripts/api_server.py` - Run the API
- `frontend/pages/index.tsx` - Web interface

**Config:**
- `requirements.txt` - Python packages
- `.env.example` - Environment template
- `run_setup.bat` - Windows setup helper

---

## ⏱️ Timeline

| Time | Action | Command |
|------|--------|---------|
| **0:00** | Start here | Read this file |
| **0:05** | Install | `pip install -r requirements.txt` |
| **5:10** | Download model | `python scripts/download_model.py` |
| **10:15** | Start server | `python scripts/api_server.py` |
| **10:30** | ✅ DONE | Test with curl/browser |
| **10:45** | Bonus: Train | `python scripts/fine_tune.py` (optional) |
| **15:45** | Bonus: UI | `cd frontend && npm install && npm run dev` (optional) |

---

## 🎓 What You're Learning

This project teaches:
- ✅ LLM fine-tuning (LoRA technique)
- ✅ Model quantization & optimization
- ✅ API design & FastAPI
- ✅ Frontend integration (React/Next.js)
- ✅ Full-stack AI deployment
- ✅ Local processing (no cloud APIs)

---

## 🚀 Ready to Start?

1. **First time?** → Read `PROJECT_SUMMARY.md` for full context
2. **Want step-by-step?** → Follow `SETUP.md`
3. **Ready to code?** → Run the 3 commands above
4. **Need API docs?** → Open `http://localhost:8000/docs`

---

## 💬 Key Points

- **500M parameters** = tiny model, fast training
- **LoRA** = efficient fine-tuning, saves time & memory
- **<100ms** = inference is super fast locally
- **M drive only** = keeps everything organized
- **No APIs** = privacy-first, no external calls
- **Production ready** = can deploy immediately

---

## ✨ Success Looks Like

After Step 3, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Then curl works and returns JSON with extracted entities.

**That's it. You're running NER extraction locally!**

---

## 🎬 For Your Video

Key talking points:
1. **Problem**: Need to extract structured data locally
2. **Solution**: Tiny model (500M) + LoRA + FastAPI
3. **Result**: Sub-100ms extraction, no APIs, completely private
4. **Impact**: Can be deployed on any VPS, used in any pipeline

---

## 📞 Quick Links

| What | Where |
|------|-------|
| Full docs | `README.md` |
| Setup guide | `SETUP.md` |
| Project breakdown | `PROJECT_SUMMARY.md` |
| API docs (live) | http://localhost:8000/docs |
| Web UI | http://localhost:3000 |

---

**🎉 You've got everything you need. Let's go!**

Start with: `pip install -r requirements.txt`

Questions? Check `SETUP.md` section "Troubleshooting"
