from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from loguru import logger
import pickle
import os
from app.config import Config


class Recommender:
    """ 
    TF-IDF recommender system using Nearest Neighbors 
    """
    def __init__(self, documents: list, k: int = 3, metric: str = 'cosine'):
        self.documents = documents
        self.k = k
        self.metric = metric
        self._create_or_load_tfidf()
        self._create_knn()

    def _create_or_load_tfidf(self):
        if not os.path.isfile(Config.doc_word_path):
            self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
            self.tfidf_matrix = self.vectorizer.fit_transform(documents)
            with open(Config.doc_word_path, "wb") as f:
                pickle.dump(self.tfidf_matrix, f)
            logger.debug('TF-IDF matrix created and saved.')
            with open(Config.vectorizer_path, "wb") as f:
                pickle.dump(self.vectorizer, f)
            logger.debug('Vectorizer created and saved.')
        else:
            with open(Config.doc_word_path, "rb") as f:
                self.tfidf_matrix = pickle.load(f)
            logger.debug('TF-IDF matrix loaded.')
            with open(Config.vectorizer_path, "rb") as f:
                self.vectorizer = pickle.load(f)
            logger.debug('Vectorizer loaded.')

    def _create_knn(self):
        """ 
        Create the KNN model 
        """
        self.knn = NearestNeighbors(n_neighbors=self.k, metric=self.metric)
        self.knn.fit(self.tfidf_matrix)

    def recommend(self, new_document: list) -> list:
        """
        Recommend similar documents based on the new document.
        """
        new_tfidf = self.vectorizer.transform(new_document)
        _, indices = self.knn.kneighbors(new_tfidf)
        return [self.documents[i] for i in indices.flatten()]


if __name__== '__main__':
    # Example documents
    documents = {"doc1": "Machine learning is powerful",
                "doc2": "Deep learning is a subset of machine learning",
                "doc3": "Natural language processing is part of AI",
                "doc4": "AI is evolving with deep learning",
                "doc5": "Machine learning and AI are transforming industries",
                "doc6": "Machine learning is the future",
                "doc7": "Deep learning is the future",
                "doc8": "AI is the future of nothing",
                "doc9": "The dog is brown",
                "doc10": "The cat is black",
                "doc11": "Cat and AI are not the same",
                "doc12": "The cat is a pet",
                "doc13": "The dog is a pet"}
    
    # Convert the dictionary to a list of documents
    documents = list(documents.values())

    recommender = Recommender(documents)

    # Example new document
    new_document = ["Machine learning is the disgusting future"]
    
    recommendations = recommender.recommend(new_document)
    
    print("Recommended documents for the new document:")
    for doc in recommendations:
        print(doc)