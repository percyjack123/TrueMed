from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "TrueMed",
        "status": "Backend running"
    })

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    image.save(os.path.join(UPLOAD_FOLDER, image.filename))

    # MOCK RESULT (replace later with real ML)
    is_fake = random.choice([True, False])
    confidence = round(random.uniform(70, 95), 2)

    return jsonify({
    "project": "TrueMed",
    "visual_blur_ok": random.choice([True, False]),
    "batch_id_valid": random.choice([True, False]),
    "confidence": round(random.uniform(75, 95), 2)
})


if __name__ == "__main__":
    app.run(debug=True)
