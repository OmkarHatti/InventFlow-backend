from fastapi import Depends, FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import ProductValidate
from DB_Model import Base, ProductDB
from database import engine, SessionLocal
import DB_Model as DB_Model
from sqlalchemy.orm import Session
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("images"):
    os.makedirs("images")

app.mount("/images", StaticFiles(directory="images"), name="images")

Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Hello World I am Omkar"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Initial dummy data
# products = [
#     ProductValidate(id=1, name="Soap", description="Washing", price=200, quantity=2),
#     ProductValidate(id=2, name="Shampoo", description="Hair care", price=350, quantity=5),
# ]

# def init():
#     db = SessionLocal()
#     count = db.query(DB_Model.ProductDB).count()
#     if count == 0:
#         for product in products:
#             db.add(DB_Model.ProductDB(**product.model_dump(), image_url=""))
#     db.commit()
#     db.close()

# init()


@app.get("/Products/")
def all_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()


@app.get("/Products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == id).first()
    if product:
        return product
    return {"error": "Product not found"}


@app.post("/Products/")
async def add_product(
    id: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    image_path = ""

    if image:
        file_path = f"images/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = file_path

    new_product = ProductDB(
        id=id,
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image_url=image_path,
    )

    db.add(new_product)
    db.commit()

    return {"message": "Product added", "image_url": image_path}


@app.put("/Products/{id}")
async def update_product(
    id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    product = db.query(ProductDB).filter(ProductDB.id == id).first()

    if not product:
        return {"error": "Product not found"}

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    if image:
        file_path = f"images/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        product.image_url = file_path

    db.commit()

    return {"message": "Product updated"}


@app.delete("/Products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == id).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Deleted"}