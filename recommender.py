from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from loguru import logger
import pickle
import os
from config import Config

class Recommender:
    """ 
    TF-IDF recommender system using Nearest Neighbors 
    """
    def __init__(self, documents: dict, k: int = 3, metric: str = 'cosine'):
        self.documents = documents  
        self.k = k
        self.metric = metric

    def create_tfidf_vectorizer(self):
        " Create the TF-IDF matrix and vectorizer from documents."
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)  # Initialize the vectorizer
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)  # Create the TF-IDF matrix
        with open(Config.doc_word_path, "wb") as f:
            pickle.dump(self.tfidf_matrix, f)
        logger.debug('TF-IDF matrix created and saved.')
        with open(Config.vectorizer_path, "wb") as f:
            pickle.dump(self.vectorizer, f)
        logger.debug('Vectorizer created and saved.')

    def load_tfidf_mtx(self):
        " Load the TF-IDF matrix and vectorizer from disk."
        if os.path.isfile(Config.doc_word_path) and os.path.isfile(Config.vectorizer_path):
            with open(Config.doc_word_path, "rb") as f:
                tfidf_matrix = pickle.load(f)
            logger.debug('TF-IDF matrix loaded.')
            return tfidf_matrix

    def load_vectorizer(self):
        " Load the vectorizer from disk."
        if os.path.isfile(Config.vectorizer_path):
            with open(Config.vectorizer_path, "rb") as f:
                vectorizer = pickle.load(f)
            logger.debug('Vectorizer loaded.')
            return vectorizer

    def recommend(self, new_document: list) -> list:
        """
        Recommend similar documents based on the new document.
        """
        logger.debug(f"New document for recommendation: {new_document}")
        new_tfidf = self.load_vectorizer().transform(new_document)
        tfidf_matrix = self.load_tfidf_mtx()
        knn = NearestNeighbors(n_neighbors=self.k, metric=self.metric)
        fitted_model = knn.fit(tfidf_matrix)
        scores, indices = fitted_model.kneighbors(new_tfidf)
        logger.debug(f"Scores: {scores}, Indices: {indices}")
        recommendations = {}
        #extract from dictionary of documents
        for idx in indices[0]:
            doc_id = list(self.documents.keys())[idx]
            recommendations[doc_id] = self.documents[doc_id]
        logger.debug(f"Recommendations: {recommendations}")
        return recommendations
