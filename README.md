
# TrueMed — AI-Powered Medicine Counterfeit Detection System

## Overview

TrueMed is an AI-powered healthcare application designed to identify potentially counterfeit medicine packaging using computer vision and OCR-based verification techniques.

The platform combines deep learning image classification with batch ID verification to help users assess the authenticity of pharmaceutical products before consumption.

---

## Problem Statement

Counterfeit medicines pose a significant threat to public health, particularly in regions where pharmaceutical supply chains are difficult to verify.

Traditional verification methods often require manual inspection and domain expertise, making them inaccessible to everyday consumers.

TrueMed aims to provide a fast, automated, and user-friendly solution for preliminary counterfeit detection using AI.

---

## Key Features

### Visual Authenticity Detection

- Upload medicine packaging images
- CNN-based classification model
- Detects potentially counterfeit products
- Instant prediction results

### OCR-Based Verification

- Extracts batch numbers from packaging
- Uses Tesseract OCR for text recognition
- Supports automated batch validation workflows

### Batch Verification

- CSV-based batch database lookup
- Cross-checks extracted identifiers
- Improves verification reliability

### Explainable Results

- Displays prediction outcomes clearly
- Provides confidence-based insights
- Improves transparency for end users

---

## System Architecture

```text
User Upload
      │
      ▼
React Frontend
      │
      ▼
Flask API
      │
 ┌────┴────┐
 ▼         ▼
OCR      CNN Model
(Tesseract) (TensorFlow)
 │          │
 └────┬─────┘
      ▼
Verification Engine
      │
      ▼
Prediction Result
```

---

## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS

### Backend

- Flask
- Python

### Machine Learning

- TensorFlow
- Convolutional Neural Networks (CNN)

### OCR

- Tesseract OCR

### Model Hosting

- Hugging Face

---

## Workflow

1. User uploads a medicine package image.
2. Image is sent to the Flask backend.
3. TensorFlow model analyzes packaging authenticity.
4. OCR extracts batch information.
5. Batch ID is verified against stored records.
6. Results are returned to the user interface.

---

## Future Enhancements

- Multi-language packaging support
- Mobile application integration
- Barcode and QR-code verification
- Pharmaceutical database integration
- Advanced explainable AI visualizations

---

## Tech Highlights

- Full-stack React + Flask architecture
- TensorFlow-based image classification
- OCR-powered text extraction
- Dynamic model loading from Hugging Face
- Healthcare-focused AI application

---

## License

MIT License
````
