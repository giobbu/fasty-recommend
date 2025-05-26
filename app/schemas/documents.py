from pydantic import BaseModel

class AllDocuments(BaseModel):
    """
    Schema for the documents response.
    """
    message: str
    data: dict


class Document(BaseModel):
    """
    Schema for the document to be added.
    """
    data: str 