from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: int
    username: str
    hashed_password: str


class UserOut(BaseModel):
    id: int
    username: str


class Chat(BaseModel):
    id: int
    user_id1: int
    user_id2: int


class Message(BaseModel):
    id: int
    user_id: int
    chat_id: int
    content: str
    created: datetime