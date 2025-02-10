import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    text = ""

    # Essayons d'extraire le texte directement avec PyPDF2 (pour PDF non aplatis)
    try:
        print(f"Extraction du texte du fichier PDF non aplati : {pdf_path}")
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Erreur avec PyPDF2 : {e}")

    # Si le texte extrait est vide, utilisons l'OCR avec pytesseract pour PDF aplati
    if not text.strip():
        try:
            print(f"Extraction du texte du fichier PDF aplati : {pdf_path}")
            images = convert_from_path(pdf_path)
            for image in images:
                text += pytesseract.image_to_string(image)
        except Exception as e:
            print(f"Erreur avec Tesseract OCR : {e}")
    
    return text


