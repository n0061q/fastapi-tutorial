from typing import Annotated

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=200
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    tags: set[str] = set()
    avatar: Image | None = None
    pictures: list[Image]


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, lt=10)],
    # importance: Annotated[int, Body(ge=0, le=100)],
    q: Annotated[str | None, Query(min_length=3)] = None,
    item: Annotated[Item | None, Body(embed=True)] = None,
    # user: User = ...,
):
    results = {
        "item_id": item_id,
        # "user": user,
        # "importance": importance
    }
    if q:
        results.update(q=q)
    if item:
        results.update(item=item)
    return results


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    # print(weights)
    return weights
