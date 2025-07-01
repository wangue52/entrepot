from sqlalchemy import Column, Integer, String, ForeignKey,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid 
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=True)
    
    prices = relationship("Price", back_populates="product")
    product_sale_points = relationship("ProductSalePoint", back_populates="product")

class SalePoint(Base):
    __tablename__ = "sale_points"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=True)
    website = Column(String, nullable=True)
    type = Column(String, nullable=True)
    
    prices = relationship("Price", back_populates="sale_point")
    product_sale_points = relationship("ProductSalePoint", back_populates="sale_point")

class Price(Base):
    __tablename__ = "prices"
    
    id_product = Column(Integer, ForeignKey("products.id"), primary_key=True)
    id_sale_point = Column(Integer, ForeignKey("sale_points.id"), primary_key=True)
    id_date = Column(Integer, ForeignKey("dates.id"), primary_key=True)
    price = Column(Float, nullable=False)
    product = relationship("Product", back_populates="prices")
    sale_point = relationship("SalePoint", back_populates="prices")
    date = relationship("Date", back_populates="prices")

class ProductSalePoint(Base):
    __tablename__ = "product_sale_points"
    
    id_product = Column(Integer, ForeignKey("products.id"), primary_key=True)
    id_sale_point = Column(Integer, ForeignKey("sale_points.id"), primary_key=True)
    
    product = relationship("Product", back_populates="product_sale_points")
    sale_point = relationship("SalePoint", back_populates="product_sale_points")

class Date(Base):
    __tablename__ = "dates"
    
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)    
    prices = relationship("Price", back_populates="date")
