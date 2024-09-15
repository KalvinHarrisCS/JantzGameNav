# Functions/ocr.py

import pytesseract
from PIL import Image
import os

class OCRProcessor:
    def __init__(self):
        # If Tesseract is not in your PATH, specify the location directly
        # For Windows users, uncomment and set the path to your Tesseract executable
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def extract_text(self, image_path):
        try:
            print(f"Performing OCR on {image_path}...")
            text = pytesseract.image_to_string(Image.open(image_path))
            print("OCR completed successfully.")
            return text
        except Exception as e:
            print(f"An error occurred during OCR: {e}")
            return ""
