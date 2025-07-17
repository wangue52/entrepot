# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case, text, and_, or_
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import models
import schemas

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def to_dict(instance):
    """Convertit une instance SQLAlchemy en dictionnaire"""
    if not instance:
        return None
    return {c.key: getattr(instance, c.key) for c in instance.__table__.columns}

# ============================================================================
# CRUD POUR LES PRODUITS
# ============================================================================

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        title=product.title,
        link=product.link
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_products_count(db: Session):
    return db.query(models.Product).count()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

def get_product_prices(db: Session, product_id: int):
    return db.query(models.Price).filter(models.Price.id_product == product_id).all()

def search_products(
    db: Session, 
    title: Optional[str] = None, 
    min_prices: Optional[int] = None
):
    query = db.query(models.Product)
    
    if title:
        query = query.filter(models.Product.title.ilike(f"%{title}%"))
    
    if min_prices:
        subquery = (
            db.query(
                models.Price.id_product,
                func.count(models.Price.id_product).label("price_count")
            )
            .group_by(models.Price.id_product)
            .subquery()
        )
        
        query = (
            query
            .join(subquery, models.Product.id == subquery.c.id_product)
            .filter(subquery.c.price_count >= min_prices)
        )
    
    return query.all()

# ============================================================================
# CRUD POUR LES POINTS DE VENTE
# ============================================================================

def create_sale_point(db: Session, sale_point: schemas.SalePointCreate):
    db_sale_point = models.SalePoint(**sale_point.dict())
    db.add(db_sale_point)
    db.commit()
    db.refresh(db_sale_point)
    return db_sale_point

def get_sale_point(db: Session, sale_point_id: int):
    return db.query(models.SalePoint).filter(models.SalePoint.id == sale_point_id).first()

def get_sale_points(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    city: Optional[str] = None,
    type: Optional[str] = None
):
    query = db.query(models.SalePoint)
    
    if city:
        query = query.filter(models.SalePoint.city == city)
    if type:
        query = query.filter(models.SalePoint.type == type)
    
    return query.offset(skip).limit(limit).all()

def get_sale_points_count(
    db: Session, 
    city: Optional[str] = None,
    type: Optional[str] = None
):
    query = db.query(models.SalePoint)
    
    if city:
        query = query.filter(models.SalePoint.city == city)
    if type:
        query = query.filter(models.SalePoint.type == type)
    
    return query.count()

def update_sale_point(db: Session, sale_point_id: int, sale_point: schemas.SalePointUpdate):
    db_sale_point = get_sale_point(db, sale_point_id)
    if not db_sale_point:
        return None
    
    for key, value in sale_point.dict(exclude_unset=True).items():
        setattr(db_sale_point, key, value)
    
    db.commit()
    db.refresh(db_sale_point)
    return db_sale_point

def delete_sale_point(db: Session, sale_point_id: int):
    db_sale_point = get_sale_point(db, sale_point_id)
    if db_sale_point:
        db.delete(db_sale_point)
        db.commit()
        return True
    return False

# ============================================================================
# CRUD POUR LES DATES
# ============================================================================

def create_date(db: Session, date_data: schemas.DateCreate):
    db_date = models.Date(**date_data.dict())
    db.add(db_date)
    db.commit()
    db.refresh(db_date)
    return db_date

def create_date_from_iso(db: Session, date_iso: str):
    try:
        date_obj = datetime.strptime(date_iso, "%Y-%m-%d").date()
        db_date = models.Date(
            day=date_obj.day,
            month=date_obj.month,
            year=date_obj.year
        )
        db.add(db_date)
        db.commit()
        db.refresh(db_date)
        return db_date
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def get_date(db: Session, date_id: int):
    return db.query(models.Date).filter(models.Date.id == date_id).first()

def get_dates(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    year: Optional[int] = None,
    month: Optional[int] = None
):
    query = db.query(models.Date)
    
    if year:
        query = query.filter(models.Date.year == year)
    if month:
        query = query.filter(models.Date.month == month)
    
    return query.offset(skip).limit(limit).all()

def delete_date(db: Session, date_id: int):
    db_date = get_date(db, date_id)
    if db_date:
        db.delete(db_date)
        db.commit()
        return True
    return False

# ============================================================================
# CRUD POUR LES PRIX
# ============================================================================

def create_price(db: Session, price: schemas.PriceCreate):
    db_price = models.Price(
        id_product=price.id_product,
        id_sale_point=price.id_sale_point,
        id_date=price.id_date,
        price=price.price
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
  

def get_price(db: Session,product_id: int,sale_point_id: int,date_id: int):
    return(
        db.query(models.Price)
        .filter(
            models.Price.id_product == product_id,
            models.Price.id_sale_point == sale_point_id,
            models.Price.id_date == date_id)
        ).first()
    
	
def get_prices(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    product_id: Optional[int] = None,
    sale_point_id: Optional[int] = None,
    date_id: Optional[int] = None
) -> List[models.Price]:
    query = db.query(models.Price)
    if product_id is not None:
        query = query.filter(models.Price.id_product == product_id)
    if sale_point_id is not None:
        query = query.filter(models.Price.id_sale_point == sale_point_id)
    if date_id is not None:
        query = query.filter(models.Price.id_date == date_id)
    return query.offset(skip).limit(limit).all()

def get_prices_count(db: Session):
    return db.query(models.Price).count()

def delete_price(db: Session, product_id: int, sale_point_id: int, date_id: int):
    db_price = get_price(db, product_id, sale_point_id, date_id)
    if db_price:
        db.delete(db_price)
        db.commit()
        return True
    return False

def get_price_history(
    db: Session, 
    product_id: int, 
    sale_point_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    query = (
        db.query(
            models.Date.id.label("date_id"),
            models.Date.day,
            models.Date.month,
            models.Date.year,
            models.Price.price,
            models.SalePoint.id.label("sale_point_id"),
            models.SalePoint.name.label("sale_point_name")
        )
        .join(models.Date, models.Price.id_date == models.Date.id)
        .join(models.SalePoint, models.Price.id_sale_point == models.SalePoint.id)
        .filter(models.Price.id_product == product_id)
        .order_by(models.Date.year, models.Date.month, models.Date.day)
    )
    
    if sale_point_id:
        query = query.filter(models.Price.id_sale_point == sale_point_id)
    
    if start_date:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        query = query.filter(
            and_(
                models.Date.year >= start_date_obj.year,
                models.Date.month >= start_date_obj.month,
                models.Date.day >= start_date_obj.day
            )
        )
    
    if end_date:
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        query = query.filter(
            and_(
                models.Date.year <= end_date_obj.year,
                models.Date.month <= end_date_obj.month,
                models.Date.day <= end_date_obj.day
            )
        )
    
    # Transformer les résultats en structure appropriée
    results = query.all()
    price_history = []
    
    for r in results:
        price_history.append({
            "date": {
                "id": r.date_id,
                "day": r.day,
                "month": r.month,
                "year": r.year
            },
            "price": r.price,
            "sale_point": {
                "id": r.sale_point_id,
                "name": r.sale_point_name
            }
        })
    
    return price_history

def get_price_comparison(
    db: Session, 
    product_id: int, 
    specific_date: Optional[str] = None
):
    if specific_date:
        date_obj = datetime.strptime(specific_date, "%Y-%m-%d").date()
        date_record = (
            db.query(models.Date)
            .filter(
                models.Date.year == date_obj.year,
                models.Date.month == date_obj.month,
                models.Date.day == date_obj.day
            )
            .first()
        )
        if not date_record:
            return []
        date_filter = date_record.id
    else:
        latest_date = (
            db.query(func.max(models.Date.id))
            .select_from(models.Price)
            .filter(models.Price.id_product == product_id)
            .scalar()
        )
        if not latest_date:
            return []
        date_filter = latest_date
    
    return (
        db.query(
            models.SalePoint.id.label("sale_point_id"),
            models.SalePoint.name.label("sale_point_name"),
            models.Price.price,
            models.Date.id.label("date_id")
        )
        .join(models.SalePoint, models.Price.id_sale_point == models.SalePoint.id)
        .join(models.Date, models.Price.id_date == models.Date.id)
        .filter(
            models.Price.id_product == product_id,
            models.Price.id_date == date_filter
        )
        .all()
    )

# ============================================================================
# CRUD POUR LES ASSOCIATIONS PRODUIT-POINT DE VENTE
# ============================================================================

def create_product_sale_point(db: Session, psp: schemas.ProductSalePointCreate):
    db_psp = models.ProductSalePoint(**psp.dict())
    db.add(db_psp)
    db.commit()
    db.refresh(db_psp)
    return db_psp

def get_product_sale_point(db: Session, product_id: int, sale_point_id: int):
    return (
        db.query(models.ProductSalePoint)
        .filter(
            models.ProductSalePoint.id_product == product_id,
            models.ProductSalePoint.id_sale_point == sale_point_id
        )
        .first()
    )

def get_product_sale_points(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    product_id: Optional[int] = None,
    sale_point_id: Optional[int] = None
):
    query = db.query(models.ProductSalePoint)
    
    if product_id:
        query = query.filter(models.ProductSalePoint.id_product == product_id)
    if sale_point_id:
        query = query.filter(models.ProductSalePoint.id_sale_point == sale_point_id)
    
    return query.offset(skip).limit(limit).all()

def delete_product_sale_point(db: Session, product_id: int, sale_point_id: int):
    db_psp = get_product_sale_point(db, product_id, sale_point_id)
    if db_psp:
        db.delete(db_psp)
        db.commit()
        return True
    return False

# ============================================================================
# STATISTIQUES ET ANALYSE
# ============================================================================

def get_products_with_prices_count(db: Session):
    return (
        db.query(models.Price.id_product)
        .distinct()
        .count()
    )

def get_products_by_sale_point_count(db: Session):
    return (
        db.query(
            models.SalePoint.name,
            func.count(models.ProductSalePoint.id_product).label("product_count")
        )
        .join(models.ProductSalePoint, models.SalePoint.id == models.ProductSalePoint.id_sale_point)
        .group_by(models.SalePoint.name)
        .all()
    )

def get_sale_points_by_city(db: Session):
    return (
        db.query(
            models.SalePoint.city,
            func.count(models.SalePoint.id).label("sale_point_count")
        )
        .group_by(models.SalePoint.city)
        .all()
    )

def get_sale_points_by_type(db: Session):
    return (
        db.query(
            models.SalePoint.type,
            func.count(models.SalePoint.id).label("sale_point_count")
        )
        .group_by(models.SalePoint.type)
        .all()
    )

def get_prices_by_month(db: Session):
    return (
        db.query(
            models.Date.year,
            models.Date.month,
            func.count(models.Price.id_product).label("price_count"),
            func.avg(models.Price.price).label("avg_price")
        )
        .join(models.Date, models.Price.id_date == models.Date.id)
        .group_by(models.Date.year, models.Date.month)
        .order_by(models.Date.year, models.Date.month)
        .all()
    )

def get_average_prices_by_product(db: Session):
    return (
        db.query(
            models.Product.title,
            func.avg(models.Price.price).label("avg_price"),
            func.min(models.Price.price).label("min_price"),
            func.max(models.Price.price).label("max_price")
        )
        .join(models.Price, models.Product.id == models.Price.id_product)
        .group_by(models.Product.title)
        .all()
    )

def get_price_evolution(db: Session, product_id: int):
    """Retourne l'évolution du prix d'un produit au fil du temps"""
    return (
        db.query(
            models.Date.id.label("date_id"),
            models.Date.year,
            models.Date.month,
            models.Date.day,
            func.avg(models.Price.price).label("avg_price"),
            func.min(models.Price.price).label("min_price"),
            func.max(models.Price.price).label("max_price")
        )
        .join(models.Price, models.Price.id_date == models.Date.id)
        .filter(models.Price.id_product == product_id)
        .group_by(models.Date.id, models.Date.year, models.Date.month, models.Date.day)
        .order_by(models.Date.year, models.Date.month, models.Date.day)
        .all()
    )

def get_city_price_comparison(db: Session, product_id: int):
    """Compare les prix d'un produit par ville"""
    # Créer une sous-requête pour les dernières dates
    subquery = (
        db.query(
            models.Price.id_sale_point,
            func.max(models.Date.id).label("max_date_id")
        )
        .join(models.Date, models.Price.id_date == models.Date.id)  # Jointure explicite ici
        .filter(models.Price.id_product == product_id)
        .group_by(models.Price.id_sale_point)
        .subquery()
    )
    
    # Requête principale avec jointures explicites
    return (
        db.query(
            models.SalePoint.city,
            func.avg(models.Price.price).label("avg_price"),
            func.min(models.Price.price).label("min_price"),
            func.max(models.Price.price).label("max_price")
        )
        .join(subquery, and_(
            models.Price.id_sale_point == subquery.c.id_sale_point,
            models.Price.id_date == subquery.c.max_date_id
        ))
        .join(models.SalePoint, models.Price.id_sale_point == models.SalePoint.id)  # Jointure explicite
        .filter(models.Price.id_product == product_id)
        .group_by(models.SalePoint.city)
        .all()
    )
# Ajoutez cette fonction dans crud.py

def get_price_details(
    db: Session, 
    sale_point_id: Optional[int] = None,
    limit: int = 100
):
    """Récupère les prix avec les détails complets (produit + date)"""
    query = (
        db.query(
            models.Price,
            models.Product,
            models.Date
        )
        .join(models.Product, models.Price.id_product == models.Product.id)
        .join(models.Date, models.Price.id_date == models.Date.id)
    )
    
    if sale_point_id:
        query = query.filter(models.Price.id_sale_point == sale_point_id)
        
    results = query.limit(limit).all()
    
    # Transformer les résultats en format détaillé
    price_details = []
    for price, product, date in results:
        price_details.append({
            "id": price.id,
            "price": price.price,
            "date": {
                "id": date.id,
                "day": date.day,
                "month": date.month,
                "year": date.year
            },
            "product": {
                "id": product.id,
                "title": product.title,
                "link": product.link
            }
        })
    
    return price_details
def get_price_trends(db: Session, days: int = 30):
    """Analyse les tendances de prix sur une période donnée"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    return (
        db.query(
            models.Product.title,
            func.avg(models.Price.price).label("avg_price"),
            (func.max(models.Price.price) - func.min(models.Price.price)).label("price_variation"),
            func.max(models.Price.price).label("max_price"),
            func.min(models.Price.price).label("min_price")
        )
        .join(models.Date, models.Price.id_date == models.Date.id)
        .join(models.Product, models.Price.id_product == models.Product.id)
        .filter(
            and_(
                models.Date.year >= start_date.year,
                models.Date.month >= start_date.month,
                models.Date.day >= start_date.day,
                models.Date.year <= end_date.year,
                models.Date.month <= end_date.month,
                models.Date.day <= end_date.day
            )
        )
        .group_by(models.Product.title)
        .order_by(func.avg(models.Price.price).desc())
        .all()
    )

# ============================================================================
# FONCTIONS POUR L'ENDPOINT DE SANTÉ
# ============================================================================

def check_db_connection(db: Session):
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False