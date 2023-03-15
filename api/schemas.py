from pydantic import BaseModel, validator, Field


class DataFromFile(BaseModel):
    sku: str | int

    @validator('sku', pre=True, always=True, each_item=True)
    def sku_only_digits(cls, value):
        if type(value) == str:
            if not value.isdigit():
                raise ValueError('Must be Numeric')
        return value


class Product(BaseModel):
    article: str = Field(..., alias='id')
    brand: str
    title: str = Field(..., alias='name')


class ProductInput(BaseModel):
    data: dict
    params: dict
    state: int

    def products(self) -> Product:
        products = self.data.get('products', [])
        product = [Product(id=p['id'], name=p['name'], brand=p['brand']) for p in products][0]
        return product
