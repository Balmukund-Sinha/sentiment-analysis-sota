
from huggingface_hub import HfApi, create_repo
import sys

def setup_hf(token, username, repo_name, space_name):
    api = HfApi(token=token)
    
    # 1. Create Model Repo
    print(f"🛠️ Creating Model Repo: {username}/{repo_name}...")
    try:
        api.create_repo(repo_id=f"{username}/{repo_name}", repo_type="model", exist_ok=True)
        print("✅ Model Repo ready.")
    except Exception as e:
        print(f"❌ Error creating model repo: {e}")
    
    # 2. Create Space
    print(f"🛠️ Creating Space: {username}/{space_name}...")
    try:
        api.create_repo(
            repo_id=f"{username}/{space_name}", 
            repo_type="space", 
            space_sdk="docker", 
            exist_ok=True,
            private=False
        )
        print("✅ Space ready.")
    except Exception as e:
        print(f"❌ Error creating space: {e}")

    # 3. Set Space Secrets
    print(f"🔐 Setting Space Secret: MODEL_PATH...")
    try:
        api.add_space_secret(
            repo_id=f"{username}/{space_name}",
            key="MODEL_PATH",
            value=f"{username}/{repo_name}"
        )
        print("✅ Secret set.")
    except Exception as e:
        print(f"❌ Error setting secret: {e}")

if __name__ == "__main__":
    TOKEN = "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"
    USERNAME = "mukundsinha"
    REPO_NAME = "sentiment-deberta-v3"
    SPACE_NAME = "sentiment-api"
    
    setup_hf(TOKEN, USERNAME, REPO_NAME, SPACE_NAME)
