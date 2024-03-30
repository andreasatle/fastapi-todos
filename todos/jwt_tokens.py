from pydantic import BaseModel
from jose import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import todos.models as models


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JWTToken:
    def __init__(self, jwt_secret_key: str = None, jwt_algorithm: str = None, duration: timedelta = timedelta(minutes=15)):
        load_dotenv()

        self.secret_key = os.getenv("JWT_SECRET_KEY", jwt_secret_key)
        self.algorithm = os.getenv("JWT_ALGORITHM", jwt_algorithm)
        self.duration = duration

        if self.secret_key is None:
            raise ValueError("jwt_secret_key variable not set")
        if self.algorithm is None:
            raise ValueError("jwt_algorithm variable not set")

    def encode(self, user: models.Users) -> str:
        payload = {
            "sub": user.username,
            "exp": datetime.utcnow() + self.duration,
            "id": user.id,
        }
        return Token(access_token=jwt.encode(payload, self.secret_key, algorithm=self.algorithm))

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
