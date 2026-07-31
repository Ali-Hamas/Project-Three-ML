#!/usr/bin/env python3
"""
Simple LoRA fine-tuning on tiny-gpt2.
No complex trainer - just simple training loop.
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import get_peft_model, LoraConfig, TaskType
from torch.utils.data import DataLoader, Dataset
import time

print("🚀 Fine-tuning tiny-gpt2 with LoRA")

# Load model from cache (instant, no download)
print("⏳ Loading model...")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
tokenizer.pad_token = tokenizer.eos_token  # Set pad token
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

# Training data (A1 Tech Solution)
training_texts = [
    "Kamran Haider is the Founder and CEO of A1 Tech Solution, a specialized software engineering and automation agency.",
    "Ali Hamas is an Agentic AI Expert specializing in CrewAI and LangChain at A1 Tech Solution.",
    "Mehdia Humais is a Full Stack Developer at A1 Tech Solution working with React and FastAPI.",
    "Contact A1 Tech Solution at agency@theaset.com or call +92 321 7719831 for AI automation services.",
    "A1 Tech Solution delivered the LogiQuest Dispatch Automator, replacing 5 hours of daily manual dispatcher workload.",
    "The AI LearnHub LMS by A1 Tech Solution serves 10k+ students with automated Stripe billing integrations.",
    "A1 Tech Solution built the A1 Voiceflow Platform integrating Twilio and ElevenLabs for voice AI.",
    "Britsync AI is an autonomous workspace built by A1 Tech Solution for B2B lead generation and market intelligence.",
    "A1 Tech Solution's AI Call Agent pipeline uses Twilio SIP to call leads and log scheduled bookings.",
    "The Discord AI Bot powered by Gemini 2.0 translates voice commands into workflows for A1 Tech Solution clients.",
    "John Smith works at Google in Mountain View.",
    "Alice Johnson is a software engineer at Microsoft in Seattle.",
]

print(f"⏳ Preparing training data... {len(training_texts)} samples")

# Simple tokenization
class SimpleDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=128):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )

    def __len__(self):
        return len(self.encodings["input_ids"])

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels": self.encodings["input_ids"][idx]
        }

dataset = SimpleDataset(training_texts, tokenizer)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
print(f"✅ Dataset created: {len(dataset)} samples")

# Simple training loop
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
        # Move to device
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        # Forward pass
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        epoch_loss += loss.item()

        # Backward pass
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
output_dir = r"M:\MCHINE LERNING\Project one\models\fine_tuned"
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"""
✅ Fine-tuning complete!

📊 Results:
   - Model saved: {output_dir}
   - LoRA adapters: adapter_model.bin, adapter_config.json
   - Total training steps: {step}
   - Final epoch loss: {avg_epoch_loss:.4f}
   - Training time: ~2 minutes
   - Ready for deployment!
""")
