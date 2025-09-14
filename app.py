import base64
import io
from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import cv2
import numpy as np

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Ghost\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

@app.route('/')
def index():
    return render_template('index.html')

def preprocess_image(pil_image):
    # Convert PIL image to OpenCV format
    cv_image = np.array(pil_image.convert("RGB"))
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

    # Increase size for small text
    scale_factor = 2
    cv_image = cv2.resize(cv_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # Apply adaptive thresholding (better than fixed threshold for varied backgrounds)
    cv_image = cv2.adaptiveThreshold(cv_image, 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 35, 15)

    # Remove small noise
    kernel = np.ones((1, 1), np.uint8)
    cv_image = cv2.morphologyEx(cv_image, cv2.MORPH_OPEN, kernel)
    cv_image = cv2.medianBlur(cv_image, 3)

    # Sharpen image
    sharpen_kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
    cv_image = cv2.filter2D(cv_image, -1, sharpen_kernel)

    # Convert back to PIL for Tesseract
    processed_pil = Image.fromarray(cv_image)
    return processed_pil

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()

    if 'image' not in data:
        return jsonify({"error": "No image provided"}), 400

    image_data = data['image'].split(',')[1]
    selections = data.get("selections", [])
    lang = data.get("lang", "eng")

    try:
        img_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(img_bytes))

        extracted_text = ""
        if selections:
            for sel in selections:
                x, y, w, h = map(int, (sel["x"], sel["y"], sel["width"], sel["height"]))
                cropped = image.crop((x, y, x + w, y + h))
                processed = preprocess_image(cropped)
                extracted_text += pytesseract.image_to_string(processed, lang=lang, config="--oem 3 --psm 6") + "\n"
        else:
            processed = preprocess_image(image)
            extracted_text = pytesseract.image_to_string(processed, lang=lang, config="--oem 3 --psm 6")

        return jsonify({"text": extracted_text.strip()})

    except Exception as e:
        print(f"[OCR Error]: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
