from pydantic import BaseModel

class Users(BaseModel):
    usernames: list[str]
