from os import getenv
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")

class CONFIGURATION(BaseSettings):
    ENGINE_URL :  str = getenv("DATABASE_PATH")
    TOKEN_EXPIRE_TIME : int = getenv("TOKEN_EXPIRE_TIME")
    SECRET_KEY : str = getenv("SECRET_KEY")
    ALGORITHM : str = getenv("ALGORITHM")
