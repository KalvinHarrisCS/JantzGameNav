# Functions/ui/ocr.py

import pytesseract
from PIL import Image
import sys

class OCRProcessor:
    def __init__(self):
        # If Tesseract is not in your PATH, specify the location directly
        if sys.platform.startswith('win'):
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        elif sys.platform.startswith('darwin'):
            pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Adjust if different
        else:
            pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust if different
        pass

    def extract_text(self, image_path):
        try:
            print(f"Performing OCR on {image_path}...")
            text = pytesseract.image_to_string(Image.open(image_path))
            print("OCR completed successfully.")
            # Filter out dashes and vertical bars
            filtered_text = text.replace("-", "").replace("|", "")
            return filtered_text
        except Exception as e:
            print(f"An error occurred during OCR: {e}")
            return ""
