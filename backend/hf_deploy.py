
import os
from huggingface_hub import HfApi

def deploy(token, username, space_name, model_repo):
    api = HfApi(token=token)
    
    # 1. Upload Code to Space
    print(f"🚀 Uploading Codebase to Space: {username}/{space_name}...")
    try:
        # Uploading specific files to avoid bloat and large model files in the Space repo
        files_to_upload = [
            "Dockerfile",
            "requirements.txt",
            "calibration.py",
            "README.md",
        ]
        
        # Upload individual files
        for file in files_to_upload:
            if os.path.exists(file):
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=file,
                    repo_id=f"{username}/{space_name}",
                    repo_type="space"
                )
        
        # Upload backend directory
        api.upload_folder(
            folder_path="backend",
            path_in_repo="backend",
            repo_id=f"{username}/{space_name}",
            repo_type="space",
            ignore_patterns=["__pycache__/*", "*.pyc"]
        )
        print("✅ Codebase uploaded to Space.")
    except Exception as e:
        print(f"❌ Code upload failed: {e}")

    # 2. Upload Model to Model Repo
    print(f"🚀 Uploading Model to Hub: {username}/{model_repo}...")
    try:
        api.upload_folder(
            folder_path="deberta_sentiment_model",
            repo_id=f"{username}/{model_repo}",
            repo_type="model"
        )
        print("✅ Model uploaded to Hub.")
    except Exception as e:
        print(f"❌ Model upload failed: {e}")

if __name__ == "__main__":
    TOKEN = "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"
    USERNAME = "mukundsinha"
    SPACE_NAME = "sentiment-api"
    MODEL_REPO = "sentiment-deberta-v3"
    
    deploy(TOKEN, USERNAME, SPACE_NAME, MODEL_REPO)
