from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    """
    rest api config 
    """
    doc_db_path: str = "app/db/doc.json"
    doc_word_path: str = "app/db/doc_word.pickle"
    vectorizer_path: str = "app/db/vectorizer.pickle"

@dataclass(frozen=True)
class Recommender:
    """ 
    recommender config
    """
    k : int = 3
    metric : str = 'cosine'
