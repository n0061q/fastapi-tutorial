from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def get_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            alias="query",
            # deprecated=True,
            # include_in_schema=False,
        ),
    ]
):
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        data.update({"q": q})
    return data
