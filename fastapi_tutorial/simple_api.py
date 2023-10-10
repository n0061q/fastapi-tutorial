from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI


DB_FILE_NAME = "database.db"


engine = create_engine(
    f"sqlite:///{DB_FILE_NAME}", echo=True, connect_args={"check_same_thread": False}
)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    # Path(DB_FILE_NAME).unlink(missing_ok=True)
    create_db_and_tables()


@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero):
    with Session(engine) as s:
        s.add(hero)
        s.commit()
        s.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes() -> list[Hero]:
    with Session(engine) as s:
        return s.exec(select(Hero)).all()
