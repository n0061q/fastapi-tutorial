from typing import Annotated

from fastapi import FastAPI, Query, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, lt=10)],
    size: Annotated[float, Query(gt=0, le=2.5)],
    q: Annotated[str | None, Query(min_length=3)] = None,
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results
