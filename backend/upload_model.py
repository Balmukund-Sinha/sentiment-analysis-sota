
import os
import sys
import argparse
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def upload_model(model_path, repo_name, token=None):
    """
    Uploads a local fine-tuned model to the Hugging Face Hub.
    """
    print(f"🚀 Loading model from {model_path}...")
    try:
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    print(f"📦 Uploading to Hugging Face Hub: {repo_name}...")
    try:
        # This will create the repo if it doesn't exist
        model.push_to_hub(repo_name, use_auth_token=token)
        tokenizer.push_to_hub(repo_name, use_auth_token=token)
        print(f"✅ Successfully uploaded to: https://huggingface.co/{repo_name}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print("💡 Make sure you have the 'huggingface_hub' library installed and are logged in via 'huggingface-cli login'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload fine-tuned model to Hugging Face Hub")
    parser.add_argument("--model_path", type=str, required=True, help="Path to local model directory")
    parser.add_argument("--repo_name", type=str, required=True, help="Hugging Face repo name (e.g., 'username/my-model')")
    parser.add_argument("--token", type=str, default=None, help="Hugging Face API token (optional if logged in via CLI)")

    args = parser.parse_args()
    upload_model(args.model_path, args.repo_name, args.token)
