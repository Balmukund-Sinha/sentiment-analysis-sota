
import os
import time
from huggingface_hub import HfApi

def deploy():
    token = "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"
    repo_id = "mukundsinha/sentiment-api"
    api = HfApi(token=token)
    
    print(f"🧹 Cleaning up incorrect paths in {repo_id}...")
    try:
        files = api.list_repo_files(repo_id=repo_id, repo_type="space")
        for f in files:
            if "\\" in f:
                print(f"  Deleting corrupt path: {f}")
                api.delete_file(path_in_repo=f, repo_id=repo_id, repo_type="space")
    except Exception as e:
        print(f"  Cleanup warning: {e}")

    print(f"🚀 Forcing Upload of Production Codebase...")
    
    # 1. Root files
    root_files = {
        "Dockerfile_HF": "Dockerfile",
        "requirements.txt": "requirements.txt",
        "calibration.py": "calibration.py",
        "backend/README_SPACE.md": "README.md"
    }
    
    for local, remote in root_files.items():
        if os.path.exists(local):
            print(f"  Uploading {local} -> {remote}")
            api.upload_file(
                path_or_fileobj=local,
                path_in_repo=remote,
                repo_id=repo_id,
                repo_type="space"
            )

    # 2. Backend folder
    backend_files = ["app.py", "engine.py", "explainability.py", "explainability_shap.py"]
    for f in backend_files:
        local_path = os.path.join("backend", f)
        if os.path.exists(local_path):
            print(f"  Uploading {local_path} -> backend/{f}")
            api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=f"backend/{f}",
                repo_id=repo_id,
                repo_type="space"
            )

    print("✅ DEPLOYMENT COMPLETE. Waiting for rebuild...")

if __name__ == "__main__":
    deploy()
