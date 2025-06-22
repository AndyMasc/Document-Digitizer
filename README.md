# OCR Image Uploader with Flask and Dropzone

This project is a web application built with Flask and Dropzone.js that allows users to upload images via drag-and-drop, processes the images with OCR (Optical Character Recognition) using Tesseract, and extracts text content from the images.

---

## Features

- Drag-and-drop image upload with visual feedback using Dropzone.js
- Server-side image processing with OpenCV and Tesseract OCR
- Text extraction from uploaded images
- Clean, minimal Flask backend with templated HTML interface
- Automatic file management: temporary files are removed after processing

---

## Technologies Used

- Python 3.x
- Flask (web framework)
- Flask-Dropzone (Dropzone.js integration for Flask)
- OpenCV (image processing)
- Tesseract OCR (text extraction)
- HTML, CSS, JavaScript (frontend)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ocr-image-uploader.git
   cd ocr-image-uploader

2.  **Create and activate venv
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows

3. Install tesseract and pytesseract

