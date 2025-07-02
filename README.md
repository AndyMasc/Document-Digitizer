# OCR Image Uploader with Flask and Dropzone

This project is a web application built with Flask and Dropzone.js that allows users to upload images of their handwriting or documents via drag-and-drop or file selector, processes the images with OCR (Optical Character Recognition) using cloud vision, and extracts text content from the images making it a PDF.

Convert your: 
reciepts, documents, nutrition labels, handwritings, report cards, passports, certificates, notes and more.

---

# Demo

To demo this project, visit the url: https://digitit.koyeb.app/
---

## Features

- Drag-and-drop image upload with visual feedback using Dropzone.js
- Server-side image processing with OpenCV and cloud vision OCR
- Safe, files are only used locally, and deleted from server after use
- Text extraction from uploaded images
- Clean, minimal Flask backend with templated HTML interface
- Automatic file management: temporary files are removed after processing

---

## Technologies Used

- Python 3.13
- Flask
- cloud vision OCR (text extraction)
- HTML, CSS, JavaScript (frontend)

---

## AI

AI was utilized to help make this project - although, for debugging. It was utilized to debug why formatting of the original image "broke" when converted to a PDF and how to fix it. Also utilized to debug why the Pytesseract model was not being installed properly on my computer, and created the scanner image on the upload page.

---
