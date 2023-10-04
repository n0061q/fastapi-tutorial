from typing import Annotated

from fastapi import FastAPI, Cookie, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    ads_id: Annotated[str | None, Cookie()] = None,
    x_special_header: Annotated[list[str] | None, Header()] = list(),
):
    return {"ads_id": ads_id, "X-Special-Header": x_special_header}
