from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import Response, RedirectResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = 1.99
    tags: list[str] = []


class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None


class UserIn(UserOut):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> UserOut:
    # By declaring response model / return type as UserOut
    # we make sure that password is not included in the reponse
    # FastAPI does the data filtering
    return user


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> dict:
    data = item.model_dump()
    data["tags"].append("created by X")
    data["price"] += 1
    return data


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0, tags=["kek"]),
        Item(name="Plumbus", price=32.0, tax=2),
    ]


@app.get("/portal/")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse({"message": "Here is your interdimentional portal."})


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
