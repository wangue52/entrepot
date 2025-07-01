# schemas.py
from pydantic import BaseModel, Field, field_validator,ConfigDict
from typing import List, Optional, Dict, Any
from datetime import date
from enum import Enum
from datetime import datetime, timedelta
# ============================================================================
# MODÈLES DE BASE
# ============================================================================

class ProductBase(BaseModel):
    title: str = Field(..., max_length=255, description="Nom du produit")
    link: Optional[str] = Field(None, description="Lien vers le produit")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
   pass

class Product(ProductBase):
    id: int
    
    class Config:
         model_config = ConfigDict(from_attributes=True)

class SalePointBase(BaseModel):
    name: str = Field(..., max_length=255, description="Nom du point de vente")
    city: Optional[str] = Field(None, max_length=100, description="Ville du point de vente")
    website: Optional[str] = Field(None, description="Site web du point de vente")
    type: Optional[str] = Field(None, max_length=50, description="Type de point de vente")

class SalePointCreate(SalePointBase):
    pass

class SalePointUpdate(SalePointBase):
    pass

class SalePoint(SalePointBase):
    id: int
    
    class Config:
       model_config = ConfigDict(from_attributes=True)
class DateBase(BaseModel):
    day: int = Field(..., ge=1, le=31, description="Jour du mois")
    month: int = Field(..., ge=1, le=12, description="Mois")
    year: int = Field(..., ge=2000, le=2100, description="Année")

class DateCreate(DateBase):
    pass

class Date(DateBase):
    id: int
    
    class Config:
       model_config = ConfigDict(from_attributes=True)
class PriceBase(BaseModel):
    id_product: int = Field(..., description="ID du produit")
    id_sale_point: int = Field(..., description="ID du point de vente")
    id_date: int = Field(..., description="ID de la date")
    price: float = Field(..., gt=0, description="Prix du produit")

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    class Config:
       model_config = ConfigDict(from_attributes=True)

class ProductSalePointBase(BaseModel):
    id_product: int = Field(..., description="ID du produit")
    id_sale_point: int = Field(..., description="ID du point de vente")

class ProductSalePointCreate(ProductSalePointBase):
    pass

class ProductSalePoint(ProductSalePointBase):
    class Config:
       model_config = ConfigDict(from_attributes=True)
# ============================================================================
# MODÈLES DE RÉPONSE AVANCÉS
# ============================================================================

class PriceDetail(Price):
    product: Product
    sale_point: SalePoint
    date: Date

    class Config:
       model_config = ConfigDict(from_attributes=True)
class PriceComparison(BaseModel):
    sale_point_id: int
    sale_point_name: str
    price: float
    date_id: int

    class Config:
           model_config = ConfigDict(from_attributes=True)

# ============================================================================
# MODÈLES POUR LES STATISTIQUES
# ============================================================================

class ProductsBySalePoint(BaseModel):
    name: str
    product_count: int

class SalePointsByCity(BaseModel):
    city: str
    sale_point_count: int

class SalePointsByType(BaseModel):
    type: str
    sale_point_count: int

class PricesByMonth(BaseModel):
    year: int
    month: int
    price_count: int
    avg_price: float

class AveragePricesByProduct(BaseModel):
    title: str
    avg_price: float
    min_price: float
    max_price: float

class PriceEvolution(BaseModel):
    date_id: int
    year: int
    month: int
    day: int
    avg_price: float
    min_price: float
    max_price: float

class CityPriceComparison(BaseModel):
    city: str
    avg_price: float
    min_price: float
    max_price: float

class PriceTrend(BaseModel):
    title: str
    avg_price: float
    price_variation: float
    max_price: float
    min_price: float

# ============================================================================
# MODÈLES POUR LES RÉPONSES PAGINÉES
# ============================================================================

class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[Any]

# Exemples d'implémentations spécifiques
class PaginatedProducts(PaginatedResponse):
    data: List[Product]

class PaginatedSalePoints(PaginatedResponse):
    data: List[SalePoint]

class PaginatedDates(PaginatedResponse):
    data: List[Date]

class PaginatedPrices(PaginatedResponse):
    data: List[Price]

class PaginatedProductSalePoints(PaginatedResponse):
    data: List[ProductSalePoint]

# ============================================================================
# MODÈLES POUR LES RÉPONSES D'ERREUR
# ============================================================================

class ErrorResponse(BaseModel):
    detail: str

class ValidationError(BaseModel):
    loc: List[str]
    msg: str
    type: str

class HTTPError(BaseModel):
    detail: List[ValidationError] | str

# ============================================================================
# ENUMS POUR LES FILTRES
# ============================================================================

class SalePointType(str, Enum):
    supermarket = "supermarket"
    electronics = "electronics"
    clothing = "clothing"
    online = "online"
    other = "other"

# ============================================================================
# VALIDATEURS PERSONNALISÉS
# ============================================================================



class DateISO(BaseModel):
    date: str

    @field_validator('date')
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

# Résolution des références circulaires
Price.model_rebuild()
Product.model_rebuild()
SalePoint.model_rebuild()
Date.model_rebuild()
ProductSalePoint.model_rebuild()