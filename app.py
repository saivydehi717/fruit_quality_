from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import io, base64, os, webbrowser, threading
from PIL import Image

app = Flask(__name__)
CORS(app)

# Auto-detect classes
train_dir = "dataset/train"
class_names = sorted(os.listdir(train_dir))
print(f"✅ Loaded {len(class_names)} classes: {class_names}")

# Load best model if available
model_path = "model/best_fruit_model.h5" if os.path.exists("model/best_fruit_model.h5") else "model/fruit_model.h5"
model = load_model(model_path)
print(f"✅ Model loaded: {model_path}")

# --- Helpers ---
def get_quality(class_name):
    # ALWAYS check on RAW class name before any cleaning
    name = class_name.lower()
    if name.startswith("rotten") or "_rotten" in name or "rotten_" in name:
        return "rotten"
    if "nonfruit" in name or "non_fruit" in name:
        return "nonfruit"
    nonfruit_keywords = ["car","bottle","building","chair","bus","cat","dog","laptop","mobile","phone","table","person","hand","background"]
    if any(k in name for k in nonfruit_keywords):
        return "nonfruit"
    return "fresh"

def clean_name(class_name):
    # Clean ONLY for display — quality is already determined from raw name
    name = class_name.lower()
    # Remove rotten prefix first
    if name.startswith("rotten_"):
        name = name[7:]  # remove "rotten_"
    for r in ["_fruit","nonfruit_","fruit_","non_fruit_"]:
        name = name.replace(r, "")
    return name.replace("_", " ").strip().title()

# --- Routes ---
@app.route("/", methods=["GET"])
def home():
    return send_file("fruit_detection.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data or "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        img_data = data["image"]
        if "," in img_data:
            img_data = img_data.split(",")[1]

        img = Image.open(io.BytesIO(base64.b64decode(img_data))).convert("RGB").resize((224, 224))
        arr = np.expand_dims(np.array(img) / 255.0, axis=0)

        preds = model.predict(arr, verbose=0)[0]
        top3 = np.argsort(preds)[::-1][:3]

        top_class = class_names[top3[0]]
        confidence = int(preds[top3[0]] * 100)
        quality = get_quality(top_class)   # quality from RAW class name
        display_name = clean_name(top_class)  # display name without rotten/fresh prefix

        print(f"DEBUG → raw class: {top_class} | quality: {quality} | display: {display_name}")

        if confidence < 40:
            description = f"Low confidence — try a clearer image"
        else:
            q_label = quality.capitalize()
            description = f"{display_name} detected — {q_label} ({confidence}% confidence)"

        return jsonify({
            "fruit": display_name,
            "quality": quality,
            "confidence": confidence,
            "description": description,
            "top_predictions": [
                {"name": clean_name(class_names[i]), "confidence": int(preds[i] * 100)}
                for i in top3
            ]
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("🚀 Starting Fruit Quality Detection Server...")
    print("🌐 Opening at http://127.0.0.1:5000")
    threading.Timer(1.5, open_browser).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
