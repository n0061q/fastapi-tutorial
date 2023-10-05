from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field

app = FastAPI()


class It(BaseModel):
    value: str | None = Field(max_length=10, default=None)


@app.get("/it/", status_code=status.HTTP_418_IM_A_TEAPOT)
async def get_it(response: Response, q:bool = False):
    if q:
        response.status_code = status.HTTP_200_OK
    return "You got it!"


@app.post("/it/", status_code=201)
async def post_it(it: It):
    return f"Posted it: {it!r}"
