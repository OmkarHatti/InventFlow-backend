from pydantic import BaseModel

class ProductValidate(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    image_url: str   # ✅ just store path or URL