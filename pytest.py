# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test du point de contrôle de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "API is running successfully"}

def test_create_product():
    """Test de création d'un produit"""
    product_data = {
        "id": "test-product-1",
        "title": "Test Product",
        "link": "https://example.com/test-product"
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Product"

def test_get_products():
    """Test de récupération des produits"""
    response = client.get("/products/")
    assert response.status_code == 200
    assert "products" in response.json()
    assert "total" in response.json()

def test_create_sale_point():
    """Test de création d'un point de vente"""
    sale_point_data = {
        "id": "test-sp-1",
        "name": "Test Sale Point",
        "city": "Test City",
        "website": "https://example.com",
        "type": "online"
    }
    response = client.post("/sale-points/", json=sale_point_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Sale Point"

def test_get_sale_points():
    """Test de récupération des points de vente"""
    response = client.get("/sale-points/")
    assert response.status_code == 200
    assert "sale_points" in response.json()

def test_create_date():
    """Test de création d'une date"""
    date_data = {
        "id": "2024-01-15",
        "day": 15,
        "month": 1,
        "year": 2024
    }
    response = client.post("/dates/", json=date_data)
    assert response.status_code == 200
    assert response.json()["day"] == 15

def test_stats_endpoints():
    """Test des endpoints de statistiques"""
    response = client.get("/stats/products")
    assert response.status_code == 200
    
    response = client.get("/stats/sale-points")
    assert response.status_code == 200
    
    response = client.get("/stats/prices")
    assert response.status_code == 200

# Pour lancer les tests : pytest test_main.py






