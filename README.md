# Text Bot

A lightweight Flask-based OCR application for extracting text from images through a clean browser interface.

Built for fast local OCR without external APIs, cloud processing, or the ritual suffering of configuring Tesseract manually like it's still 2012.

---

## Features

### Fast Local OCR
- Fully local text extraction
- No external OCR services required
- Lightweight Python-based processing

### Multiple Image Input Methods
- Upload image files
- Drag and drop support
- Clipboard image paste
- Open images directly in browser

### Region-Based OCR
- Select specific areas on the image
- Extract only targeted text regions
- Interactive canvas selection

### Simple Browser Interface
- Clean split-layout workspace
- Instant OCR feedback
- One-click copy support

### Lightweight Setup
- No Tesseract installation required
- Minimal dependencies
- Quick local startup

---

# Preview

> A clean OCR workspace with an image canvas on the left and extracted text results on the right for fast one-step processing.

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Flask | Backend web framework |
| Pillow | Image processing |
| OpenCV | Image handling and preprocessing |
| NumPy | Array operations |
| RapidOCR | OCR engine |

---

# Installation

## Prerequisites

- Python 3.10+
- pip

---

## Install Dependencies

```bash
py -m pip install -r requirements.txt
```

---

# Run the Application

```bash
py app.py
```

---

# Open the App

Visit:

```text
http://127.0.0.1:5000
```

Because every developer eventually creates a localhost tool and briefly feels like a wizard opening portals on port 5000.

---

# How It Works

1. Upload, paste, or drag an image into the browser
2. The image is sent to the Flask backend
3. RapidOCR processes the image locally
4. Extracted text appears instantly in the results panel
5. Copy the text with one click

---

# Features in Detail

## Full Image OCR
Extract text from the entire image in a single operation.

---

## Region OCR
Select only the part of the image you want to process using interactive area selection.

Useful for:
- Screenshots
- Receipts
- Cropped documents
- Partial text detection

---

## Clipboard Support
Paste images directly from clipboard without manually saving files first.

Humanity finally invented one genuinely useful thing after centuries of war and spam emails.

---

## Fast Processing
- Lightweight browser workflow
- Minimal startup time
- Quick OCR response
- Local processing for better privacy

---

# Notes

- Runs entirely on your local machine
- No internet connection required after installation
- No external OCR API dependencies
- OCR accuracy depends on image clarity and resolution

If extraction quality drops:
- Use higher-resolution images
- Crop noisy backgrounds
- Improve contrast before upload

---

```

---

# Future Improvements

- PDF OCR support
- Multi-language OCR
- Batch image processing
- Export as TXT / DOCX
- OCR history panel
- Real-time preprocessing controls

---

---

# Author

**Harshil Vanparia | Ghost**
