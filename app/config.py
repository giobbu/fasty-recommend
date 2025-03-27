from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    """
    rest api config 
    """
    doc_db_path: str = "app/db/doc.json"
    doc_word_path: str = "app/db/doc_word.json"

@dataclass(frozen=True)
class Recommender:
    """ 
    recommender config
    """
    k : int = 3
    metric : str = 'cosine'
