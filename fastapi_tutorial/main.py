from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def post_item(item: Item):
    data = item.model_dump()
    if item.tax:
        data.update(price_with_tax=item.price + item.tax)
    return data


@app.put("/items/{item_id}")
async def put_item(item_id: int, item: Item, q: str | None = None):
    data = {"item_id": item_id, **item.model_dump()}
    if q:
        data.update(q=q)
    return data
