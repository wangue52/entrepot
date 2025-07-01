# main.py
# Ajouter en haut du fichier
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse  
from datetime import datetime
from sqlalchemy.orm import Session
import crud
import models
import schemas
from databases import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

models.Base.metadata.create_all(bind=engine)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# Créer les tables
# ... (imports restent les mêmes)

# Créer les tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Price Comparison API",
    description="API REST pour comparer les prix de produits entre différents points de vente",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En production, spécifier les domaines autorisés
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# Dépendance pour obtenir la session de base de données
# main.py




# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# ENDPOINTS DE SANTÉ
# ============================================================================

@app.get("/health", tags=["Health"], summary="Vérifie l'état de santé de l'API")
def health_check(db: Session = Depends(get_db)):
    """Vérifie la connexion à la base de données et l'état général de l'API"""
    db_status = crud.check_db_connection(db)
    return {
        "status": "OK" if db_status else "ERROR",
        "database": "connected" if db_status else "disconnected",
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# ENDPOINTS POUR LES PRODUITS
# ============================================================================

@app.post("/products/", 
          response_model=schemas.Product,
          status_code=status.HTTP_201_CREATED,
          tags=["Products"],
          summary="Créer un nouveau produit")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Crée un nouveau produit dans la base de données"""
    return crud.create_product(db, product)

@app.get("/products/", 
         response_model=List[schemas.Product],
         tags=["Products"],
         summary="Lister tous les produits")
def read_products(
    skip: int = Query(0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, description="Nombre maximum d'éléments à retourner"),
    db: Session = Depends(get_db)
):
    """Retourne une liste paginée de tous les produits"""
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", 
         response_model=schemas.Product,
         tags=["Products"],
         summary="Obtenir les détails d'un produit")
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Retourne les détails d'un produit spécifique"""
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return db_product

@app.put("/products/{product_id}", 
         response_model=schemas.Product,
         tags=["Products"],
         summary="Mettre à jour un produit")
def update_product(
    product_id: int, 
    product: schemas.ProductUpdate, 
    db: Session = Depends(get_db)
):
    """Met à jour les informations d'un produit existant"""
    updated_product = crud.update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return updated_product

@app.delete("/products/{product_id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Products"],
            summary="Supprimer un produit")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Supprime un produit de la base de données"""
    if not crud.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Produit non trouvé")

@app.get("/products/search/", 
         response_model=List[schemas.Product],
         tags=["Products"],
         summary="Recherche avancée de produits")
def search_products(
    title: Optional[str] = Query(None, description="Terme de recherche dans le titre"),
    min_prices: Optional[int] = Query(None, description="Nombre minimum de prix associés"),
    db: Session = Depends(get_db)
):
    """Recherche de produits avec filtres avancés"""
    return crud.search_products(db, title=title, min_prices=min_prices)

# ============================================================================
# ENDPOINTS POUR LES POINTS DE VENTE
# ============================================================================

@app.post("/sale-points/", 
          response_model=schemas.SalePoint,
          status_code=status.HTTP_201_CREATED,
          tags=["Sale Points"],
          summary="Créer un nouveau point de vente")
def create_sale_point(sale_point: schemas.SalePointCreate, db: Session = Depends(get_db)):
    """Crée un nouveau point de vente dans la base de données"""
    return crud.create_sale_point(db, sale_point)

@app.get("/sale-points/", 
         response_model=List[schemas.SalePoint],
         tags=["Sale Points"],
         summary="Lister tous les points de vente")
def read_sale_points(
    skip: int = Query(0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, description="Nombre maximum d'éléments à retourner"),
    city: Optional[str] = Query(None, description="Filtrer par ville"),
    type: Optional[str] = Query(None, description="Filtrer par type de point de vente"),
    db: Session = Depends(get_db)
):
    """Retourne une liste paginée de points de vente avec filtres optionnels"""
    return crud.get_sale_points(db, skip=skip, limit=limit, city=city, type=type)

@app.get("/sale-points/{sale_point_id}", 
         response_model=schemas.SalePoint,
         tags=["Sale Points"],
         summary="Obtenir les détails d'un point de vente")
def read_sale_point(sale_point_id: int, db: Session = Depends(get_db)):
    """Retourne les détails d'un point de vente spécifique"""
    db_sale_point = crud.get_sale_point(db, sale_point_id)
    if not db_sale_point:
        raise HTTPException(status_code=404, detail="Point de vente non trouvé")
    return db_sale_point

@app.put("/sale-points/{sale_point_id}", 
         response_model=schemas.SalePoint,
         tags=["Sale Points"],
         summary="Mettre à jour un point de vente")
def update_sale_point(
    sale_point_id: int, 
    sale_point: schemas.SalePointUpdate, 
    db: Session = Depends(get_db)
):
    """Met à jour les informations d'un point de vente existant"""
    updated_sale_point = crud.update_sale_point(db, sale_point_id, sale_point)
    if not updated_sale_point:
        raise HTTPException(status_code=404, detail="Point de vente non trouvé")
    return updated_sale_point

@app.delete("/sale-points/{sale_point_id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Sale Points"],
            summary="Supprimer un point de vente")
def delete_sale_point(sale_point_id: int, db: Session = Depends(get_db)):
    """Supprime un point de vente de la base de données"""
    if not crud.delete_sale_point(db, sale_point_id):
        raise HTTPException(status_code=404, detail="Point de vente non trouvé")

# ============================================================================
# ENDPOINTS POUR LES DATES
# ============================================================================

@app.post("/dates/", 
          response_model=schemas.Date,
          status_code=status.HTTP_201_CREATED,
          tags=["Dates"],
          summary="Créer une nouvelle date")
def create_date(date_data: schemas.DateCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle date dans la base de données"""
    return crud.create_date(db, date_data)

@app.post("/dates/from-iso/", 
          response_model=schemas.Date,
          status_code=status.HTTP_201_CREATED,
          tags=["Dates"],
          summary="Créer une date à partir d'une chaîne ISO")
def create_date_from_iso(
    date_iso: str = Query(..., description="Date au format ISO (YYYY-MM-DD)"), 
    db: Session = Depends(get_db)
):
    """Crée une date à partir d'une chaîne au format ISO 8601"""
    try:
        return crud.create_date_from_iso(db, date_iso)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dates/", 
         response_model=List[schemas.Date],
         tags=["Dates"],
         summary="Lister toutes les dates")
def read_dates(
    skip: int = Query(0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, description="Nombre maximum d'éléments à retourner"),
    year: Optional[int] = Query(None, description="Filtrer par année"),
    month: Optional[int] = Query(None, description="Filtrer par mois"),
    db: Session = Depends(get_db)
):
    """Retourne une liste paginée de dates avec filtres optionnels"""
    return crud.get_dates(db, skip=skip, limit=limit, year=year, month=month)

@app.get("/dates/{date_id}", 
         response_model=schemas.Date,
         tags=["Dates"],
         summary="Obtenir les détails d'une date")
def read_date(date_id: int, db: Session = Depends(get_db)):
    """Retourne les détails d'une date spécifique"""
    db_date = crud.get_date(db, date_id)
    if not db_date:
        raise HTTPException(status_code=404, detail="Date non trouvée")
    return db_date

@app.delete("/dates/{date_id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Dates"],
            summary="Supprimer une date")
def delete_date(date_id: int, db: Session = Depends(get_db)):
    """Supprime une date de la base de données"""
    if not crud.delete_date(db, date_id):
        raise HTTPException(status_code=404, detail="Date non trouvée")

# ============================================================================
# ENDPOINTS POUR LES PRIX
# ============================================================================

@app.post("/prices/", 
          response_model=schemas.Price,
          status_code=status.HTTP_201_CREATED,
          tags=["Prices"],
          summary="Créer un nouveau prix")
def create_price(price: schemas.PriceCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle entrée de prix dans la base de données"""
    # Vérifier que les entités associées existent
    if not crud.get_product(db, price.id_product):
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    if not crud.get_sale_point(db, price.id_sale_point):
        raise HTTPException(status_code=404, detail="Point de vente non trouvé")
    if not crud.get_date(db, price.id_date):
        raise HTTPException(status_code=404, detail="Date non trouvée")
    
    return crud.create_price(db, price)

@app.get("/prices/", 
         response_model=List[schemas.Price],
         tags=["Prices"],
         summary="Lister tous les prix")
def read_prices(
    skip: int = Query(0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, description="Nombre maximum d'éléments à retourner"),
    product_id: Optional[int] = Query(None, description="Filtrer par ID de produit"),
    sale_point_id: Optional[int] = Query(None, description="Filtrer par ID de point de vente"),
    date_id: Optional[int] = Query(None, description="Filtrer par ID de date"),
    db: Session = Depends(get_db)
):
    """Retourne une liste paginée de prix avec filtres optionnels"""
    return crud.get_prices(db, skip=skip, limit=limit, 
                          product_id=product_id, 
                          sale_point_id=sale_point_id, 
                          date_id=date_id)

@app.get("/prices/{product_id}/{sale_point_id}/{date_id}", 
         response_model=schemas.Price,
         tags=["Prices"],
         summary="Obtenir un prix spécifique")
def read_price(
    product_id: int, 
    sale_point_id: int, 
    date_id: int, 
    db: Session = Depends(get_db)
):
    """Retourne un prix spécifique"""
    db_price = crud.get_price(db, product_id, sale_point_id, date_id)
    if not db_price:
        raise HTTPException(status_code=404, detail="Prix non trouvé")
    return db_price

@app.delete("/prices/{product_id}/{sale_point_id}/{date_id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Prices"],
            summary="Supprimer un prix")
def delete_price(
    product_id: int, 
    sale_point_id: int, 
    date_id: int, 
    db: Session = Depends(get_db)
):
    """Supprime une entrée de prix de la base de données"""
    if not crud.delete_price(db, product_id, sale_point_id, date_id):
        raise HTTPException(status_code=404, detail="Prix non trouvé")

@app.get("/products/{product_id}/prices", 
         response_model=List[schemas.PriceDetail],
         tags=["Prices"],
         summary="Historique des prix d'un produit")
def get_price_history(
    product_id: int,
    sale_point_id: Optional[int] = Query(None, description="Filtrer par point de vente"),
    start_date: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Retourne l'historique des prix pour un produit spécifique"""
    return crud.get_price_history(db, product_id, sale_point_id, start_date, end_date)

@app.get("/products/{product_id}/price-comparison", 
         response_model=List[schemas.PriceComparison],
         tags=["Prices"],
         summary="Comparaison des prix pour un produit")
def get_price_comparison(
    product_id: int,
    specific_date: Optional[str] = Query(None, description="Date spécifique (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Compare les prix d'un produit entre différents points de vente"""
    return crud.get_price_comparison(db, product_id, specific_date)

# ============================================================================
# ENDPOINTS POUR LES ASSOCIATIONS PRODUIT-POINT DE VENTE
# ============================================================================

@app.post("/product-sale-points/", 
          response_model=schemas.ProductSalePoint,
          status_code=status.HTTP_201_CREATED,
          tags=["Product-SalePoint Associations"],
          summary="Créer une nouvelle association produit-point de vente")
def create_product_sale_point(
    psp: schemas.ProductSalePointCreate, 
    db: Session = Depends(get_db)
):
    """Crée une nouvelle association entre un produit et un point de vente"""
    # Vérifier que les entités existent
    if not crud.get_product(db, psp.id_product):
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    if not crud.get_sale_point(db, psp.id_sale_point):
        raise HTTPException(status_code=404, detail="Point de vente non trouvé")
    
    return crud.create_product_sale_point(db, psp)

@app.get("/product-sale-points/", 
         response_model=List[schemas.ProductSalePoint],
         tags=["Product-SalePoint Associations"],
         summary="Lister toutes les associations")
def read_product_sale_points(
    skip: int = Query(0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, description="Nombre maximum d'éléments à retourner"),
    product_id: Optional[int] = Query(None, description="Filtrer par ID de produit"),
    sale_point_id: Optional[int] = Query(None, description="Filtrer par ID de point de vente"),
    db: Session = Depends(get_db)
):
    """Retourne une liste paginée d'associations produit-point de vente"""
    return crud.get_product_sale_points(db, skip=skip, limit=limit, 
                                      product_id=product_id, 
                                      sale_point_id=sale_point_id)

@app.get("/product-sale-points/{product_id}/{sale_point_id}", 
         response_model=schemas.ProductSalePoint,
         tags=["Product-SalePoint Associations"],
         summary="Obtenir une association spécifique")
def read_product_sale_point(
    product_id: int, 
    sale_point_id: int, 
    db: Session = Depends(get_db)
):
    """Retourne une association spécifique entre un produit et un point de vente"""
    db_psp = crud.get_product_sale_point(db, product_id, sale_point_id)
    if not db_psp:
        raise HTTPException(status_code=404, detail="Association non trouvée")
    return db_psp

@app.delete("/product-sale-points/{product_id}/{sale_point_id}", 
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Product-SalePoint Associations"],
            summary="Supprimer une association")
def delete_product_sale_point(
    product_id: int, 
    sale_point_id: int, 
    db: Session = Depends(get_db)
):
    """Supprime une association entre un produit et un point de vente"""
    if not crud.delete_product_sale_point(db, product_id, sale_point_id):
        raise HTTPException(status_code=404, detail="Association non trouvée")

# ============================================================================
# ENDPOINTS POUR LES STATISTIQUES
# ============================================================================

@app.get("/stats/products-with-prices-count", 
         response_model=int,
         tags=["Statistics"],
         summary="Nombre de produits avec des prix")
def get_products_with_prices_count(db: Session = Depends(get_db)):
    """Retourne le nombre de produits ayant au moins un prix associé"""
    return crud.get_products_with_prices_count(db)

@app.get("/stats/products-by-sale-point", 
         response_model=List[schemas.ProductsBySalePoint],
         tags=["Statistics"],
         summary="Nombre de produits par point de vente")
def get_products_by_sale_point_count(db: Session = Depends(get_db)):
    """Retourne le nombre de produits par point de vente"""
    return crud.get_products_by_sale_point_count(db)

@app.get("/stats/sale-points-by-city", 
         response_model=List[schemas.SalePointsByCity],
         tags=["Statistics"],
         summary="Nombre de points de vente par ville")
def get_sale_points_by_city(db: Session = Depends(get_db)):
    """Retourne le nombre de points de vente par ville"""
    return crud.get_sale_points_by_city(db)

@app.get("/stats/sale-points-by-type", 
         response_model=List[schemas.SalePointsByType],
         tags=["Statistics"],
         summary="Nombre de points de vente par type")
def get_sale_points_by_type(db: Session = Depends(get_db)):
    """Retourne le nombre de points de vente par type"""
    return crud.get_sale_points_by_type(db)

@app.get("/stats/prices-by-month", 
         response_model=List[schemas.PricesByMonth],
         tags=["Statistics"],
         summary="Statistiques de prix par mois")
def get_prices_by_month(db: Session = Depends(get_db)):
    """Retourne des statistiques sur les prix par mois"""
    return crud.get_prices_by_month(db)

@app.get("/stats/average-prices-by-product", 
         response_model=List[schemas.AveragePricesByProduct],
         tags=["Statistics"],
         summary="Prix moyens par produit")
def get_average_prices_by_product(db: Session = Depends(get_db)):
    """Retourne les prix moyens, min et max par produit"""
    return crud.get_average_prices_by_product(db)

@app.get("/stats/products/{product_id}/price-evolution", 
         response_model=List[schemas.PriceEvolution],
         tags=["Statistics"],
         summary="Évolution du prix d'un produit")
def get_price_evolution(product_id: int, db: Session = Depends(get_db)):
    """Retourne l'évolution historique du prix d'un produit"""
    return crud.get_price_evolution(db, product_id)

@app.get("/stats/products/{product_id}/city-comparison", 
         response_model=List[schemas.CityPriceComparison],
         tags=["Statistics"],
         summary="Comparaison des prix par ville")
def get_city_price_comparison(product_id: int, db: Session = Depends(get_db)):
    """Compare les prix d'un produit entre différentes villes"""
    return crud.get_city_price_comparison(db, product_id)

@app.get("/stats/price-trends", 
         response_model=List[schemas.PriceTrend],
         tags=["Statistics"],
         summary="Tendances de prix récentes")
def get_price_trends(
    days: int = Query(30, description="Nombre de jours à analyser"),
    db: Session = Depends(get_db)
):
    """Analyse les tendances de prix sur une période donnée"""
    return crud.get_price_trends(db, days)

# ============================================================================
# DOCUMENTATION ALTERNATIVE
# ============================================================================

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


