from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


db_file_name = "database.db"
engine = create_engine(
    f"sqlite:///{db_file_name}", echo=True, connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    # Path(db_file_name).unlink(missing_ok=True)
    create_db_and_tables()


@app.post("/heroes/")
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
