FROM python:3.11

WORKDIR /app

# Install Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

COPY . /app

RUN pip install -r requirements.txt