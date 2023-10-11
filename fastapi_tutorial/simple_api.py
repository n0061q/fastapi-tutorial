from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI


DB_FILE_NAME = "database.db"


engine = create_engine(
    f"sqlite:///{DB_FILE_NAME}", echo=True, connect_args={"check_same_thread": False}
)


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroCreate(HeroBase):
    secret_name: str = ""


class HeroRead(HeroBase):
    id: int
    secret_name: str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    # Path(DB_FILE_NAME).unlink(missing_ok=True)
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate):
    with Session(engine) as s:
        db_hero = Hero.from_orm(hero)
        s.add(db_hero)
        s.commit()
        s.refresh(db_hero)
        return db_hero


@app.get("/heroes/", response_model=list[HeroRead])
def read_heroes():
    with Session(engine) as s:
        return s.exec(select(Hero)).all()
