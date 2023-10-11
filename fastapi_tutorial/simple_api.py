from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException, status, Query


DB_FILE_NAME = "database.db"


engine = create_engine(
    f"sqlite:///{DB_FILE_NAME}", echo=True, connect_args={"check_same_thread": False}
)


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


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
def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as s:
        return s.exec(select(Hero).offset(offset).limit(limit)).all()


@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int):
    with Session(engine) as s:
        hero = s.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hero not found")
        return hero
