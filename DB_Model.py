from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class ProductDB(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)
    image_url = Column(String(255))  # ✅ store path