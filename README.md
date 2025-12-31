TrueMed — Medicine Counterfeit Detection System

TrueMed is an AI-powered web application for detecting counterfeit medicine packaging using:

Deep Learning (CNN)

OCR-based batch verification

Explainable decision logic

Key Features

Visual authenticity detection using a trained CNN

Batch number extraction using OCR (Tesseract)

Batch validation using a verified CSV database

Explainable results with clear reasons

Web-based interface (React + Flask)

Model Hosting

The trained model is hosted on Hugging Face and dynamically loaded at runtime to avoid repository size constraints.

Tech Stack

Frontend: React, Vite, Tailwind CSS

Backend: Flask, TensorFlow

OCR: Tesseract

Model Hosting: Hugging Face

Note

Batch verification depends on OCR quality and packaging clarity. Visual authenticity and batch validation together reduce false positives.
