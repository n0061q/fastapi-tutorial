# FastAPI tutorial

https://fastapi.tiangolo.com/tutorial/

Code: [main.py](./fastapi_tutorial/main.py)

## Run

```sh
poetry shell
uvicorn fastapi_tutorial.main:app --reload
```


# SQLModel tutorial

https://sqlmodel.tiangolo.com/tutorial

Code:

* [sqlmodel_demo.py](./fastapi_tutorial/sqlmodel_demo.py)
* [sqlmodel_many_to_many.py](./fastapi_tutorial/sqlmodel_many_to_many.py)



# Simple API with SQLModel

https://sqlmodel.tiangolo.com/tutorial/fastapi/

Code: [fastapi_tutorial/simple_api](./fastapi_tutorial/simple_api/)

## Run

```sh
poetry shell
uvicorn fastapi_tutorial.simple_api.main:app --reload
```
Open http://127.0.0.1:8000/docs

## Test

```sh
poetry run pytest -v
```
