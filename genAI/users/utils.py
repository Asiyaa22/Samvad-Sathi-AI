# users/utils.py
from passlib.context import CryptContext
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)
        return idinfo
    except ValueError:
        return None
