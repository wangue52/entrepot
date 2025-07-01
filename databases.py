# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données (modifiez selon votre configuration)
SQLALCHEMY_DATABASE_URL ="postgresql://postgres:ADMIN@localhost:5432/entrepots"
#SQLALCHEMY_DATABASE_URL = "sqlite:///./product_price_api.db"
# Pour PostgreSQL : "postgresql://user:password@localhost/dbname"
# Pour MySQL : "mysql://user:password@localhost/dbname"
metadata = MetaData()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


