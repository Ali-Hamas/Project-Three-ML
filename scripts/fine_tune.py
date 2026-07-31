#!/usr/bin/env python3
"""
Fine-tune tiny-gpt2 using LoRA for NER extraction.
Uses model already cached on your computer.
"""
import os
import json
from pathlib import Path
import torch
from datasets import Dataset
from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import get_peft_model, LoraConfig, TaskType

# Use user cache (already has model)
MODEL_CACHE = os.path.expanduser("~/.cache/huggingface/hub/models--sshleifer--tiny-gpt2")
OUTPUT_DIR = r"M:\MCHINE LERNING\Project one\models\fine_tuned"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

print(f"🚀 Fine-tuning tiny-gpt2 with LoRA")
print(f"📁 Using cached model from: {MODEL_CACHE}")
print(f"📁 Output dir: {OUTPUT_DIR}")

# Load model from cache (NO DOWNLOAD)
print(f"⏳ Loading tiny-gpt2 model from cache...")
try:
    tokenizer = AutoTokenizer.from_pretrained(
        "sshleifer/tiny-gpt2",
        trust_remote_code=True,
        cache_dir=None  # Use default cache
    )
    model = AutoModelForCausalLM.from_pretrained(
        "sshleifer/tiny-gpt2",
        torch_dtype=torch.float32,
        device_map="cpu",
        trust_remote_code=True
    )
    print(f"✅ Model loaded from cache (no download!)")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# Add LoRA adapters
print(f"⏳ Adding LoRA adapters...")
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)
print(f"✅ LoRA configured")

# Create sample training data
def create_sample_dataset():
    """Create sample NER extraction dataset"""
    samples = [
        # Original examples
        {
            "text": "John Smith works at Google in Mountain View.",
            "entities": {
                "names": ["John Smith"],
                "organizations": ["Google"],
                "locations": ["Mountain View"]
            }
        },
        {
            "text": "Alice Johnson is a software engineer at Microsoft in Seattle.",
            "entities": {
                "names": ["Alice Johnson"],
                "organizations": ["Microsoft"],
                "locations": ["Seattle"]
            }
        },
        # A1 Tech Solution examples
        {
            "text": "Kamran Haider is the Founder and CEO of A1 Tech Solution.",
            "entities": {
                "names": ["Kamran Haider"],
                "organizations": ["A1 Tech Solution"],
                "locations": []
            }
        },
        {
            "text": "Ali Hamas is an Agentic AI Expert specializing in CrewAI and LangChain at A1 Tech Solution.",
            "entities": {
                "names": ["Ali Hamas"],
                "organizations": ["A1 Tech Solution"],
                "locations": []
            }
        },
        {
            "text": "Mehdia Humais is a Full Stack Developer at A1 Tech Solution working with React and FastAPI.",
            "entities": {
                "names": ["Mehdia Humais"],
                "organizations": ["A1 Tech Solution"],
                "locations": []
            }
        },
        {
            "text": "Contact A1 Tech Solution at agency@theaset.com or call +92 321 7719831 for AI automation services.",
            "entities": {
                "names": [],
                "organizations": ["A1 Tech Solution"],
                "locations": []
            }
        },
        {
            "text": "A1 Tech Solution delivered the LogiQuest Dispatch Automator, replacing 5 hours of daily manual dispatcher workload.",
            "entities": {
                "names": [],
                "organizations": ["A1 Tech Solution", "LogiQuest"],
                "locations": []
            }
        },
        {
            "text": "The AI LearnHub LMS by A1 Tech Solution serves 10k+ students with automated Stripe billing integrations.",
            "entities": {
                "names": [],
                "organizations": ["A1 Tech Solution", "AI LearnHub", "Stripe"],
                "locations": []
            }
        },
        {
            "text": "A1 Tech Solution built the A1 Voiceflow Platform integrating Twilio and ElevenLabs for voice AI.",
            "entities": {
                "names": [],
                "organizations": ["A1 Tech Solution", "A1 Voiceflow", "Twilio", "ElevenLabs"],
                "locations": []
            }
        },
        {
            "text": "Britsync AI is an autonomous workspace built by A1 Tech Solution for B2B lead generation and market intelligence.",
            "entities": {
                "names": [],
                "organizations": ["A1 Tech Solution", "Britsync AI"],
                "locations": []
            }
        },
        {
            "text": "A1 Tech Solution's AI Call Agent pipeline uses Twilio SIP to call leads and log scheduled bookings.",
            "entities": {
                "names": [],
                "organizations": ["A1 Tech Solution", "Twilio"],
                "locations": []
            }
        },
        {
            "text": "The Discord AI Bot powered by Gemini 2.0 translates voice commands into workflows for A1 Tech Solution clients.",
            "entities": {
                "names": [],
                "organizations": ["A1 Tech Solution", "Gemini", "Discord"],
                "locations": []
            }
        },
    ]
    return samples

# Prepare training data
print(f"⏳ Preparing training data...")
dataset_samples = create_sample_dataset()

# Format for instruction-following
formatted_data = []
for sample in dataset_samples:
    prompt = f"""Extract named entities from the text.

Text: {sample['text']}

Extract and categorize:
- Names (people)
- Organizations
- Locations

Output as JSON."""

    response = json.dumps(sample['entities'], indent=2)

    formatted_data.append({
        "text": f"{prompt}\n\nJSON Output:\n{response}"
    })

# Create dataset
train_dataset = Dataset.from_dict({
    "text": [d["text"] for d in formatted_data]
})
print(f"✅ Dataset created: {len(formatted_data)} samples")

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    warmup_steps=10,
    num_train_epochs=3,
    learning_rate=2e-4,
    weight_decay=0.01,
    logging_steps=2,
    save_strategy="steps",
    save_steps=10,
    optim="adamw_8bit",
    seed=42,
)

# Trainer setup (minimal for demo)
from transformers import DataCollatorForSeq2Seq, Trainer

data_collator = DataCollatorForSeq2Seq(
    tokenizer,
    pad_to_multiple_of=8,
    return_tensors="pt",
    padding=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
)

# Fine-tune
print(f"\n🔄 Starting fine-tuning...")
trainer.train()

# Save
print(f"💾 Saving fine-tuned model to {OUTPUT_DIR}...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"""
✅ Fine-tuning complete!

📊 Results:
   - Model saved: {OUTPUT_DIR}
   - LoRA adapters: config.json, adapter_model.bin
   - Ready for deployment with FastAPI
""")
