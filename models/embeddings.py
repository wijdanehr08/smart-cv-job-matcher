from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Initialise le modèle de Transformer. 
        'paraphrase-multilingual-MiniLM-L12-v2' est excellent pour le français et l'anglais.
        """
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, text):
        """
        Génère les vecteurs numériques (embeddings) pour un texte donné.
        """
        if isinstance(text, str):
            text = [text]
        return self.model.encode(text)

def calculate_similarity(vec1, vec2):
    """
    Calcule la similarité cosinus entre deux vecteurs.
    """
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
