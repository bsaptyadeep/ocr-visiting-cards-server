#!/bin/bash

# Install Tesseract-OCR
apt-get update && apt-get install -y tesseract-ocr

# Run FastAPI app
uvicorn main:app --host 0.0.0.0 --port $PORT
