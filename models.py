from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    position: str  # New field

class UserIn(BaseModel):
    name: str
    email: str
    position: str
