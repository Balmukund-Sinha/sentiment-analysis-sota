import os
from huggingface_hub import HfApi, Repository

REPO_ID = "mukundsinha/sentiment-deberta-v3-3class"
SPACE_ID = "mukundsinha/sentiment-api"
MODEL_DIR = "./deberta_sentiment_3class"
TOKEN = "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"

api = HfApi()

def deploy():
    print(f"--- Uploading Model to Hub: {REPO_ID} ---")
    if not os.path.exists(MODEL_DIR):
        print(f"Error: {MODEL_DIR} not found.")
        return

    # Create Repo if not exists
    api.create_repo(repo_id=REPO_ID, token=TOKEN, exist_ok=True, repo_type="model")
    
    # Upload model files
    api.upload_folder(
        folder_path=MODEL_DIR,
        repo_id=REPO_ID,
        repo_type="model",
        token=TOKEN
    )
    print("Model upload complete.")

    print(f"--- Updating Space: {SPACE_ID} ---")
    # Upload backend files
    files_to_upload = [
        "backend/app.py",
        "backend/engine.py",
        "backend/explainability_shap.py",
        "backend/explainability.py",
        "requirements.txt",
        "Dockerfile",
        "README_SPACE.md"
    ]
    
    for f in files_to_upload:
        if os.path.exists(f):
            print(f"Uploading {f}...")
            # Hugging Face Spaces expect README.md at root
            target_path = "README.md" if f == "README_SPACE.md" else f
            api.upload_file(
                path_or_fileobj=f,
                path_in_repo=target_path,
                repo_id=SPACE_ID,
                repo_type="space",
                token=TOKEN
            )
    
    # Set Environment Variable for the Space to use the new model repo
    # This ensures the space loads the 3-class model from the Hub
    # Alternatively, we can update engine.py to prioritize this REPO_ID
    print("Deployment complete.")

if __name__ == "__main__":
    deploy()
