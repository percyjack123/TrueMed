from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
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
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # MOCK PREDICTION (temporary)
    is_fake = random.choice([True, False])
    confidence = random.uniform(70, 95)

    result = "COUNTERFEIT" if is_fake else "GENUINE"

    return jsonify({
        "project": "TrueMed",
        "result": result,
        "confidence": round(confidence, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
