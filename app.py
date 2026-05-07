import base64
import io
from flask import Flask, request, jsonify, render_template
from PIL import Image
import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR

app = Flask(__name__)

ocr_engine = RapidOCR()

@app.route('/')
def index():
    return render_template('index.html')

def preprocess_image(pil_image):
    if pil_image is None or pil_image.width == 0 or pil_image.height == 0:
        raise ValueError("Empty image region")

    image = pil_image.convert("RGB")
    cv_image = np.array(image)
    if cv_image.size == 0:
        raise ValueError("Empty image array")

    return cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)


def enhance_image_for_ocr(pil_image):
    """Create a light fallback version for clear text that the first pass misses."""
    image = pil_image.convert("RGB")
    cv_image = np.array(image)
    if cv_image.size == 0:
        raise ValueError("Empty image array")

    bgr = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # Upscale only if the source is reasonably small.
    height, width = bgr.shape[:2]
    if max(height, width) < 1400:
        bgr = cv2.resize(bgr, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def extract_text_from_image(pil_image, lang_code):
    # RapidOCR is language-agnostic for this use case, so keep the main path fast.
    processed = preprocess_image(pil_image)
    results, _ = ocr_engine(processed)

    lines = []
    if results:
        for item in results:
            if len(item) >= 2 and item[1]:
                text = str(item[1]).strip()
                if text:
                    lines.append(text)

    if lines:
        return "\n".join(lines)

    fallback = enhance_image_for_ocr(pil_image)
    results, _ = ocr_engine(fallback)
    lines = []
    if results:
        for item in results:
            if len(item) >= 2 and item[1]:
                text = str(item[1]).strip()
                if text:
                    lines.append(text)

    return "\n".join(lines)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()

    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400

    image_field = data['image']
    image_data = image_field.split(',', 1)[1] if ',' in image_field else image_field
    selections = data.get("selections", [])
    lang = data.get("lang", "eng")

    try:
        img_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_w, img_h = image.size

        extracted_text = ""
        if selections:
            chunks = []
            for sel in selections:
                x, y, w, h = map(float, (sel["x"], sel["y"], sel["width"], sel["height"]))

                # Skip accidental clicks/tiny boxes that don't represent text regions.
                if w < 2 or h < 2:
                    continue

                x1 = max(0, min(int(round(x)), img_w))
                y1 = max(0, min(int(round(y)), img_h))
                x2 = max(0, min(int(round(x + w)), img_w))
                y2 = max(0, min(int(round(y + h)), img_h))

                if x2 <= x1 or y2 <= y1:
                    continue

                cropped = image.crop((x1, y1, x2, y2))
                chunk_text = extract_text_from_image(cropped, lang)
                if chunk_text:
                    chunks.append(chunk_text)
            extracted_text = "\n".join(chunks)
        else:
            extracted_text = extract_text_from_image(image, lang)

        return jsonify({"text": extracted_text.strip()})

    except Exception as e:
        print(f"[OCR Error]: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
