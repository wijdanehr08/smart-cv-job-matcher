import re
import string

def clean_text(text):
    """
    Nettoie le texte pour le NLP tout en préservant le sens.
    """
    if not text:
        return ""
    
    # Conversion en minuscules
    text = text.lower()
    
    # Suppression des URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Suppression des emails
    text = re.sub(r'\S+@\S+', '', text)
    
    # Suppression des caractères spéciaux inutiles mais conservation des ponctuations importantes pour les Transformers
    # On garde les points et virgules car les Transformers utilisent la structure des phrases
    
    # Suppression des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_text_from_pdf(pdf_file):
    """
    Extrait le texte d'un fichier PDF.
    """
    import PyPDF2
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
