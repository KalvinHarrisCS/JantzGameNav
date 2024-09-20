# Functions/ui/ocr.py

import pytesseract
from PIL import Image
import sys
import os

class OCRProcessor:
    def __init__(self):
        if sys.platform.startswith('win'):
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.abspath(os.getcwd())

            tesseract_path = os.path.join(base_path, 'Tesseract-OCR', 'tesseract.exe')

            if not os.path.exists(tesseract_path):
                tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            if not os.path.exists(tesseract_path):
                tesseract_path = 'tesseract'

            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            pytesseract.pytesseract.tesseract_cmd = 'tesseract'

    def extract_text(self, image_path):
        try:
            print(f"Performing OCR on {image_path}...")
            text = pytesseract.image_to_string(Image.open(image_path))
            print("OCR completed successfully.")
            filtered_text = text.replace("-", "").replace("|", "")
            return filtered_text
        except Exception as e:
            print(f"An error occurred during OCR: {e}")
            return ""
