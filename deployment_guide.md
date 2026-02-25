# 🚀 Hybrid Deployment Guide (Option 4)

This guide explains how to deploy the **Sentiment Analysis System** using the "Hybrid Power" strategy: **Hugging Face Spaces** for the backend (GPU-ready) and **Vercel** for the frontend (fast CDN).

## Phase 1: Upload Model to Hugging Face Hub
Since model files are large, we host them on the Hugging Face Hub.

1.  **Install tools**: `pip install huggingface_hub transformers`
2.  **Login**: `huggingface-cli login`
3.  **Upload**:
    ```bash
    python backend/upload_model.py --model_path ./deberta_sentiment_model --repo_name your-username/sentiment-deberta-v3
    ```

---

## Phase 2: Deploy Backend (HF Spaces)
1.  **Create Space**: Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2.  **Settings**:
    - **Name**: `sentiment-api`
    - **SDK**: `Docker` (Blank)
    - **Hardware**: Choose `CPU Basic` (Free) or `T4 small` (Low cost).
3.  **Environment Variables**:
    - In Space Settings, add `MODEL_PATH` = `your-username/sentiment-deberta-v3`.
4.  **Connect Repo**: Push your code to the HF Space's Git repository. Ensure the `Dockerfile` is in the root.

---

## Phase 3: Deploy Frontend (Vercel)
1.  **Push to GitHub**: (Already done!)
2.  **Connect to Vercel**:
    - Go to [vercel.com](https://vercel.com) and import your repository.
3.  **Framework**: Vite (Auto-detected).
4.  **Environment Variables**:
    - Add `VITE_API_URL`: Use the Direct URL of your HF Space (e.g., `https://your-username-sentiment-api.hf.space`).
5.  **Deploy**: Click "Deploy".

---

## Separation of Concerns
- **Backend (HF)**: High performance, handles heavy model files and SHAP calculations.
- **Frontend (Vercel)**: Global distribution, instantaneous loading.
- **Model (HF Hub)**: Dedicated versioning and storage for ML artifacts.
