---
title: PCOS AI Diagnosis System
emoji: 🏥
colorFrom: pink
colorTo: red
sdk: docker
app_port: 7860
---
🌸 PCOS Advanced Diagnostic & Assistant System

An End-to-End Clinical Screening & Patient Support Ecosystem

This system bridges the gap between raw clinical data and patient understanding. By analyzing over 40 clinical biomarkers, it provides high-accuracy screening while offering a context-aware AI assistant to guide patients through their results.

🚀 Key Features

Predictive Diagnostics: A high-accuracy Random Forest engine (FastAPI) that analyzes hormonal, physical, and metabolic markers.

Llama 3.3 Intelligence: Integrated via Groq API for sub-second responses, providing personalized lifestyle, diet, and exercise advice.

Clinical Deep-Dive: Specialized tracking of $LH/FSH$ ratios, follicle counts (Left/Right), and metabolic indicators.

Hugging Face Integration: Live deployment for instant clinical testing and community feedback.

🏗️ Technical Architecture

The system is built on a decoupled architecture to ensure scalability and low latency:

Frontend	  Streamlit	                    Responsive UI & Interactive Data Visualization
ML Engine	  FastAPI + Scikit-Learn	    High-performance inference for diagnostic payloads
Brain	      Llama 3.3 (Groq)	Context-    aware generative AI for patient counseling
Deployment	  Docker & Hugging Face	        Containerized reliability and public accessibility

📊 Model Evaluation
We evaluated five different algorithms to ensure the highest diagnostic sensitivity (crucial for healthcare):

CatBoostClassifier(Selected): Best balance of accuracy and feature importance ranking.

XGBoost: High performance but required more hyperparameter tuning.

SVM: Effective in high-dimensional spaces but slower on inference.

Logistic Regression: Used as a baseline.

KNN: Useful for clustering but sensitive to outliers in hormonal data.


🛠️ Quick Start & Deployment

1. Live Demo
Experience the system immediately on Hugging Face Spaces:
👉 https://huggingface.co/spaces/Vijayshete04/pcos-diagnostic-ai

2. Local Installation

# Clone the repository
git clone https://github.com/Vijayshete04/pcos-diagnostic-ai.git
cd PCOS-Diagnosis-AI

# Set up your environment variables (.env)
echo "GROQ_API_KEY=your_key_here" > .env

# Run via Docker
docker build -t pcos-app .
docker run -p 8501:8501 --env-file .env pcos-app

📂 Repository Structure
app.py: The "Heart" — Streamlit logic and dashboard metrics.

chatbot.py: The "Voice" — Llama 3.3 logic and Groq integration.

main.py: The "Brain" — FastAPI backend for ML model serving.

model/: Trained weights and pre-processing pipelines.

requirements.txt: Comprehensive list of dependencies including groq, fastapi, and scikit-learn.

Disclaimer: This tool is for educational and screening assistance purposes only. It is not a replacement for professional medical diagnosis.