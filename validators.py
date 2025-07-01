# validators.py
from pydantic import validator
from typing import Optional
import re

class ProductValidator:
    @staticmethod
    def validate_title(title: str) -> str:
        if not title or len(title.strip()) < 2:
            raise ValueError("Product title must be at least 2 characters long")
        if len(title) > 255:
            raise ValueError("Product title must not exceed 255 characters")
        return title.strip()
    
    @staticmethod
    def validate_link(link: Optional[str]) -> Optional[str]:
        if not link:
            return None
        # Validation basique d'URL
        url_pattern = r'^https?://.+'
        if not re.match(url_pattern, link):
            raise ValueError("Invalid URL format")
        return link

class SalePointValidator:
    @staticmethod
    def validate_name(name: str) -> str:
        if not name or len(name.strip()) < 2:
            raise ValueError("Sale point name must be at least 2 characters long")
        if len(name) > 255:
            raise ValueError("Sale point name must not exceed 255 characters")
        return name.strip()
    
    @staticmethod
    def validate_website(website: Optional[str]) -> Optional[str]:
        if not website:
            return None
        url_pattern = r'^https?://.+'
        if not re.match(url_pattern, website):
            raise ValueError("Invalid website URL format")
        return website

class DateValidator:
    @staticmethod
    def validate_date_components(day: int, month: int, year: int) -> bool:
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")
        if not (1 <= day <= 31):
            raise ValueError("Day must be between 1 and 31")
        if not (1900 <= year <= 2100):
            raise ValueError("Year must be between 1900 and 2100")
        
        # Validation plus précise des jours selon le mois
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Gestion des années bissextiles
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            days_in_month[1] = 29
        
        if day > days_in_month[month - 1]:
            raise ValueError(f"Invalid day {day} for month {month}")
        
        return True
