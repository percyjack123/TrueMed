import tensorflow as tf
import numpy as np
import pandas as pd
import pytesseract
import re
from PIL import Image
from huggingface_hub import hf_hub_download
import os

# Explicit Tesseract path (Windows-safe)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BASE_DIR = os.path.dirname(__file__)

# ---------------- LOAD MODEL FROM HUGGING FACE ----------------
model_path = hf_hub_download(
    repo_id="SKumarii/truemed-real-fake-model",
    filename="real_fake_model.h5"
)
model = tf.keras.models.load_model(model_path)

# ---------------- LOAD BATCH DATABASE ----------------
batch_db = pd.read_csv(os.path.join(BASE_DIR, "batch_database.csv"))
batch_db["batch_number"] = (
    batch_db["batch_number"]
    .astype(str)
    .str.upper()
    .str.strip()
)

# ---------------- OCR BATCH EXTRACTION ----------------
def extract_batch_id(text: str):
    patterns = [
        r"BATCH\s*NO\.?\s*[:\-]?\s*([A-Z0-9\-]{4,15})",
        r"LOT\s*NO\.?\s*[:\-]?\s*([A-Z0-9\-]{4,15})"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).upper().strip()
    return None

# ---------------- MAIN PREDICTION ----------------
def predict_image(image_path: str):
    image = Image.open(image_path).convert("RGB")

    # ML inference
    img = image.resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    prediction = float(model.predict(img_array, verbose=0)[0][0])
    visual_blur_ok = prediction >= 0.75

    # OCR
    ocr_text = pytesseract.image_to_string(image).upper()
    extracted_batch = extract_batch_id(ocr_text)

    # Batch validation
    batch_id_valid = False
    if extracted_batch:
        batch_id_valid = extracted_batch in batch_db["batch_number"].values

    return {
        "visual_blur_ok": visual_blur_ok,
        "batch_id_valid": batch_id_valid,
        "confidence": round(prediction * 100, 2),
        "extracted_batch": extracted_batch
    }
