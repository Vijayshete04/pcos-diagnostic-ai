---
title: PCOS AI Diagnosis System
emoji: 🏥
colorFrom: pink
colorTo: red
sdk: docker
app_port: 7860
---
🩺 PCOS Advanced Diagnostic & Assistant System
An end-to-end healthcare solution that combines Machine Learning for clinical screening and Generative AI for patient support. This system analyzes 40+ clinical biomarkers to predict PCOS and provides an instant, context-aware chatbot for patient guidance.

🚀 Key Features
Predictive Diagnostics: Uses a high-accuracy ML model (FastAPI backend) to analyze hormonal, physical, and clinical markers.

Real-time AI Assistant: A specialized chatbot powered by Llama 3.3 (via Groq API) that provides personalized lifestyle, diet, and exercise advice based on the user's specific results.

Clinical Marker Analysis: Tracks complex variables including LH/FSH ratios, Follicle counts, and BMI.

Modern UI: A responsive Streamlit dashboard with interactive metrics and streaming chat responses.

Containerized: Fully Dockerized for seamless deployment.

🏗️ Technical Architecture
Frontend: Streamlit (Python) - Handles data collection and real-time visualization.

ML Backend: FastAPI - Hosts the trained model and processes diagnostic payloads.

Intelligence: Groq Cloud API - Powers the Llama 3.3 model for low-latency patient conversation.

Security: Environment-based secrets management via .env and python-dotenv.

📊 Model Performance
I compared 5 different Machine Learning models to find the most efficient diagnostic engine:

Random Forest (Selected)

Support Vector Machine (SVM)

Logistic Regression

K-Nearest Neighbors (KNN)

XGBoost

View the interactive performance charts here: [nbviewer link]

🛠️ Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/yourusername/PCOS-Diagnosis-AI.git
cd PCOS-Diagnosis-AI
2. Environment Setup
Create a .env file in the root directory:

Plaintext
GROQ_API_KEY=your_groq_api_key_here
3. Run via Docker (Recommended)
Bash
docker build -t pcos-app .
docker run -p 8501:8501 --env-file .env pcos-app
📂 Repository Structure
app.py: Main Streamlit UI and dashboard logic.

chatbot.py: Context-aware LLM logic and Groq API integration.

main.py: FastAPI backend script for ML model inference.

Dockerfile: Containerization instructions.

data/: Contains clinical datasets (Infertility and non-infertility).

⚠️ Medical Disclaimer
This system is an AI-driven screening tool, not a medical diagnosis. The results should be used for educational purposes and as a prompt to seek professional medical advice from a certified gynecologist.