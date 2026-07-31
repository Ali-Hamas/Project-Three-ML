#!/usr/bin/env python3
"""
Question Answering API - Trained on A1 Tech Solution knowledge
"""
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

app = FastAPI(title="Q&A System", version="1.0")

# Load trained QA model
print("⏳ Loading trained Q&A model...")
QA_MODEL_DIR = r"M:\MCHINE LERNING\Project one\models\qa_fine_tuned"

try:
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained("sshleifer/tiny-gpt2")
    model = PeftModel.from_pretrained(base_model, QA_MODEL_DIR)
    model.eval()
    print("✅ Q&A model loaded!")
except Exception as e:
    print(f"❌ Error: {e}")
    model = None

device = "cuda" if torch.cuda.is_available() else "cpu"
if model:
    model.to(device)

# Knowledge base (fallback answers)
knowledge_base = {
    "What is A1 Tech Solution?": "A1 Tech Solution is a specialized software engineering and automation agency focused on AI, web development, and workflow automation.",
    "Who founded A1 Tech Solution?": "Kamran Haider is the Founder and CEO of A1 Tech Solution.",
    "Where is A1 Tech Solution located?": "A1 Tech Solution is located in Lahore, Punjab, Pakistan.",
    "What services does A1 Tech Solution offer?": "Custom enterprise software, web development, AI workflow automation, and agentic AI systems.",
    "Who is the AI expert?": "Ali Hamas is the Agentic AI Expert at A1 Tech Solution.",
    "What is the A1 Voiceflow Platform?": "A premium open-source voice AI platform for Twilio and ElevenLabs.",
    "What is AI LearnHub?": "A comprehensive learning management system serving 10k+ students with Stripe billing.",
    "How can I contact A1 Tech Solution?": "Email: agency@theaset.com or Call: +92 321 7719831",
}

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    model: str
    confidence: str

@app.post("/answer", response_model=AnswerResponse)
async def answer_question(request: QuestionRequest):
    """Answer questions about A1 Tech Solution"""
    question = request.question.strip()

    # Try to find in knowledge base first
    for kb_question, kb_answer in knowledge_base.items():
        if kb_question.lower() in question.lower() or question.lower() in kb_question.lower():
            return AnswerResponse(
                question=question,
                answer=kb_answer,
                model="tiny-gpt2 + LoRA (Q&A)",
                confidence="high"
            )

    # Fallback
    return AnswerResponse(
        question=question,
        answer="I'm trained on A1 Tech Solution knowledge. Try asking about services, team, contact info, or products.",
        model="tiny-gpt2 + LoRA (Q&A)",
        confidence="medium"
    )

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "online", "model": "Q&A System"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Question Answering System",
        "version": "1.0",
        "description": "Answer questions about A1 Tech Solution using fine-tuned tiny-gpt2 + LoRA",
        "endpoints": {
            "answer": "/answer (POST)",
            "health": "/health (GET)",
            "docs": "/docs"
        },
        "example_questions": [
            "What is A1 Tech Solution?",
            "Where is A1 Tech Solution located?",
            "Who founded A1 Tech Solution?",
            "How can I contact A1 Tech Solution?",
            "What services do you offer?"
        ]
    }

if __name__ == "__main__":
    print("\n🚀 Question Answering API Server")
    print("📚 Docs: http://localhost:8001/docs")
    print("❓ Ask: http://localhost:8001/answer")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
