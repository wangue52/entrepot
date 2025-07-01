# utils.py
from datetime import datetime, date
from typing import Optional, Dict, Any
import re

def validate_date_format(date_str: str) -> bool:
    """Valide le format de date YYYY-MM-DD"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str))

def create_date_id(day: int, month: int, year: int) -> str:
    """Crée un ID de date au format YYYY-MM-DD"""
    return f"{year:04d}-{month:02d}-{day:02d}"

def parse_date_id(date_id: str) -> Dict[str, int]:
    """Parse un ID de date et retourne jour, mois, année"""
    try:
        year, month, day = map(int, date_id.split('-'))
        return {"day": day, "month": month, "year": year}
    except ValueError:
        raise ValueError(f"Invalid date format: {date_id}")

def generate_product_id(title: str) -> str:
    """Génère un ID de produit basé sur le titre"""
    # Nettoie le titre et crée un ID
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    clean_title = re.sub(r'\s+', '-', clean_title.strip())
    return f"prod-{clean_title}"

def generate_sale_point_id(name: str, city: str) -> str:
    """Génère un ID de point de vente basé sur le nom et la ville"""
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower())
    clean_name = re.sub(r'\s+', '-', clean_name.strip())
    clean_city = re.sub(r'[^a-zA-Z0-9\s]', '', city.lower())
    clean_city = re.sub(r'\s+', '-', clean_city.strip())
    return f"sp-{clean_name}-{clean_city}"

def sanitize_string(text: str) -> str:
    """Nettoie une chaîne de caractères"""
    if not text:
        return ""
    return text.strip()

def format_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Formate une réponse API standard"""
    return {
        "success": True,
        "message": message,
        "data": data
    }

def format_error_response(error: str, details: Optional[str] = None) -> Dict[str, Any]:
    """Formate une réponse d'erreur API standard"""
    response = {
        "success": False,
        "error": error
    }
    if details:
        response["details"] = details
    return response
