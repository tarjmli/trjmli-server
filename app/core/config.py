import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "SaaS i18n Automation"
    API_V1_STR: str = "/api/v1"
    GITHUB_USERNAME:str = os.getenv("GITHUB_USERNAME", "")
    

   
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1200*1200

 
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLIC_KEY: str = os.getenv("STRIPE_PUBLIC_KEY", "")

  
    GITHUB_ACCESS_TOKEN: str = os.getenv("GITHUB_ACCESS_TOKEN")
    print (GITHUB_ACCESS_TOKEN)

settings = Settings()
