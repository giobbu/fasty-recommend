from pydantic import BaseModel

class Token(BaseModel):
    " A model representing an access token and its type."
    access_token: str
    token_type: str

class TokenData(BaseModel):
    " Token data schema for user authentication "
    username: str | None = None

class User(BaseModel):
    " User schema for authentication and user management "
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    " User schema for database storage, includes hashed password "
    hashed_password: str