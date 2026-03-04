#!/bin/bash

# 1. Start FastAPI in the background on port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &
# 2. Start Streamlit on the Hugging Face port 7860
streamlit run app.py --server.port 7860 --server.address 0.0.0.0