from enum import Enum

from fastapi import FastAPI

app = FastAPI()


fake_items_db = [{"item_name": f"item-{i}"} for i in range(10)]


@app.get("/item/")
async def get_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/item/{item_id}")
async def read_item(
    item_id: str, needy: str, q: str | None = None, short: bool = False
):
    data = {"item_id": item_id, "needy": needy}
    if q:
        data.update(q=q)
    if not short:
        data.update(description="This is an amazing item that has a long description")
    return data


@app.get("/user/{user_id}/item/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    """Multiple path and query parameters (order is not important)."""
    data = {"item_id": item_id, "owner_id": user_id}
    if q:
        data.update(q=q)
    if not short:
        data.update(description="This is an amazing item that has a long description")
    return data
