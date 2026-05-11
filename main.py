from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import database
import shutil
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Images folder
if not os.path.exists("images"):
    os.makedirs("images")

app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
def greet():
    return {"message": "Hello World I am Omkar"}


# =========================
# GET ALL PRODUCTS
# =========================
@app.get("/Products/")
async def all_products():

    products = []

    async for product in database.products.find():

        product["_id"] = str(product["_id"])

        products.append(product)

    return products


# =========================
# GET PRODUCT BY ID
# =========================
@app.get("/Products/{id}")
async def get_product(id: int):

    product = await database.products.find_one({"id": id})

    if product:

        product["_id"] = str(product["_id"])

        return product

    return {"error": "Product not found"}


# =========================
# ADD PRODUCT
# =========================
@app.post("/Products/")
async def add_product(
    id: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(None),
):

    image_path = ""

    if image:
        file_path = f"images/{image.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = file_path

    product = {
        "id": id,
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
        "image_url": image_path,
    }

    await database.products.insert_one(product)

    return {
        "message": "Product added",
        "image_url": image_path
    }


# =========================
# UPDATE PRODUCT
# =========================
@app.put("/Products/{id}")
async def update_product(
    id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(None),
):

    product = await database.products.find_one({"id": id})

    if not product:
        return {"error": "Product not found"}

    image_path = product.get("image_url", "")

    if image:
        file_path = f"images/{image.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = file_path

    updated_product = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
        "image_url": image_path,
    }

    await database.products.update_one(
        {"id": id},
        {"$set": updated_product}
    )

    return {"message": "Product updated"}


# =========================
# DELETE PRODUCT
# =========================
@app.delete("/Products/{id}")
async def delete_product(id: int):

    product = await database.products.find_one({"id": id})

    if not product:
        return {"error": "Product not found"}

    await database.products.delete_one({"id": id})

    return {"message": "Deleted"}