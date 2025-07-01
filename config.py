# config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuration de la base de données
    database_url: str = "sqlite:///./product_price_api.db"
    
    # Configuration de l'API
    api_v1_str: str = "/api/v1"
    project_name: str = "Product Price Comparison API"
    version: str = "1.0.0"
    description: str = "API pour comparer les prix de produits entre différents points de vente"
    
    # Configuration de sécurité
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuration CORS
    backend_cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"

settings = Settings()