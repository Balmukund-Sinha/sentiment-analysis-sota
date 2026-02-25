
import os
from huggingface_hub import HfApi

def deploy(token, username, space_name, model_repo):
    api = HfApi(token=token)
    repo_id = f"{username}/{space_name}"
    
    # 1. Set Secret
    print(f"🔐 Setting MODEL_PATH secret in Space...")
    try:
        api.add_space_secret(repo_id=repo_id, key="MODEL_PATH", value=f"{username}/{model_repo}")
        print("✅ Secret set.")
    except Exception as e:
        print(f"❌ Could not set secret: {e}")

    # 2. Upload Files
    print(f"🚀 Uploading Codebase to Space: {repo_id}...")
    try:
        # Upload individual files in root
        for file in ["Dockerfile", "requirements.txt", "calibration.py", "README.md", "vercel.json"]:
            if os.path.exists(file):
                print(f"  Uploading {file}...")
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=file,
                    repo_id=repo_id,
                    repo_type="space"
                )
        
        # Upload backend folder
        print(f"  Uploading backend/ directory...")
        api.upload_folder(
            folder_path="backend",
            path_in_repo="backend",
            repo_id=repo_id,
            repo_type="space",
            ignore_patterns=["__pycache__/*", "*.pyc"]
        )
        
        print("✅ Complete codebase uploaded successfully.")
    except Exception as e:
        print(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    TOKEN = "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"
    USERNAME = "mukundsinha"
    SPACE_NAME = "sentiment-api"
    MODEL_REPO = "sentiment-deberta-v3"
    
    deploy(TOKEN, USERNAME, SPACE_NAME, MODEL_REPO)
