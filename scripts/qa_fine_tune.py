#!/usr/bin/env python3
"""
Fine-tune tiny-gpt2 for Question Answering on A1 Tech Solution
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import get_peft_model, LoraConfig, TaskType
from torch.utils.data import DataLoader, Dataset
import os

print("🚀 Fine-tuning tiny-gpt2 for Question Answering")

# Load model from cache
print("⏳ Loading model...")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("sshleifer/tiny-gpt2")
print("✅ Model loaded")

# Add LoRA
print("⏳ Adding LoRA adapters...")
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)
print("✅ LoRA configured")

# Q&A Training data (A1 Tech Solution)
qa_pairs = [
    ("What is A1 Tech Solution?", "A1 Tech Solution is a specialized software engineering and automation agency focused on AI, web development, and workflow automation."),
    ("Who founded A1 Tech Solution?", "Kamran Haider is the Founder and CEO of A1 Tech Solution."),
    ("Where is A1 Tech Solution located?", "A1 Tech Solution is located in Lahore, Punjab, Pakistan."),
    ("What services does A1 Tech Solution offer?", "A1 Tech Solution offers custom enterprise software, web development, AI workflow automation, and agentic AI systems."),
    ("Who is the Agentic AI Expert at A1 Tech Solution?", "Ali Hamas is the Agentic AI Expert and Chief Architect at A1 Tech Solution."),
    ("Who is the Full Stack Developer at A1 Tech Solution?", "Mehdia Humais is the Full Stack Developer at A1 Tech Solution."),
    ("What is the A1 Voiceflow Platform?", "A1 Voiceflow is a premium open-source voice AI platform and drag-and-drop workflow builder for Twilio and ElevenLabs."),
    ("What is the AI LearnHub LMS?", "AI LearnHub is a comprehensive learning management system with Stripe billing, grade books, and video progress tracking. It serves 10k+ students."),
    ("What is Britsync AI?", "Britsync AI is an autonomous workspace built by A1 Tech Solution for B2B lead generation and market intelligence."),
    ("How can I contact A1 Tech Solution?", "You can contact A1 Tech Solution at agency@theaset.com or call +92 321 7719831."),
    ("What is the AI Call Agent?", "The AI Call Agent is a pipeline that crawls leads, calls them via Twilio, qualifies intent, and logs scheduled bookings."),
    ("What is the Discord AI Bot?", "The Discord AI Bot is a voice-to-action productivity assistant powered by Gemini 2.0 that translates voice commands into workflows."),
]

print(f"⏳ Preparing Q&A training data... {len(qa_pairs)} pairs")

# Simple dataset
class QADataset(Dataset):
    def __init__(self, qa_pairs, tokenizer, max_length=128):
        self.qa_texts = []
        for q, a in qa_pairs:
            # Format: "Q: question A: answer"
            text = f"Q: {q} A: {a}"
            self.qa_texts.append(text)

        self.encodings = tokenizer(
            self.qa_texts,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )

    def __len__(self):
        return len(self.qa_texts)

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels": self.encodings["input_ids"][idx]
        }

dataset = QADataset(qa_pairs, tokenizer)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
print(f"✅ Dataset created: {len(dataset)} Q&A pairs")

# Training loop
print("\n🔄 Starting fine-tuning...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4)

num_epochs = 3
total_loss = 0
step = 0

for epoch in range(num_epochs):
    print(f"\n📊 Epoch {epoch + 1}/{num_epochs}")
    epoch_loss = 0

    for batch_idx, batch in enumerate(dataloader):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        epoch_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        step += 1
        if (batch_idx + 1) % 2 == 0:
            print(f"  Step {batch_idx + 1}: Loss = {loss.item():.4f}")

    avg_epoch_loss = epoch_loss / len(dataloader)
    print(f"✅ Epoch {epoch + 1} complete - Avg Loss: {avg_epoch_loss:.4f}")

# Save model
print("\n💾 Saving fine-tuned model...")
output_dir = r"M:\MCHINE LERNING\Project one\models\qa_fine_tuned"
os.makedirs(output_dir, exist_ok=True)
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"""
✅ Fine-tuning complete!

📊 Results:
   - Model saved: {output_dir}
   - LoRA adapters: adapter_model.bin, adapter_config.json
   - Total training steps: {step}
   - Final epoch loss: {avg_epoch_loss:.4f}
   - Trained on: {len(qa_pairs)} Q&A pairs
   - Ready for Question Answering API!
""")
