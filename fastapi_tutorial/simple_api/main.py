from typing import Annotated, Optional
from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from fastapi import FastAPI, HTTPException, status, Query, Depends


DB_FILE_NAME = "database.db"


engine = create_engine(
    f"sqlite:///{DB_FILE_NAME}", echo=True, connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


def get_db_session():
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_db_session)]


@app.on_event("startup")
def on_startup():
    # Path(DB_FILE_NAME).unlink(missing_ok=True)
    create_db_and_tables()


# Hero models


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    team: Optional["Team"] = Relationship(back_populates="heroes")


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


class HeroReadWithTeam(HeroRead):
    team: Optional["TeamRead"] = None


class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    team_id: int | None = None


# Team models


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list[Hero] = Relationship(back_populates="team")


class TeamRead(TeamBase):
    id: int


class TeamReadWithHeroes(TeamRead):
    heroes: list[HeroRead] = []


class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


# update ForwardRefs
# I wonder why this is not done automatically in SQLModel

HeroReadWithTeam.update_forward_refs()


# Path operations for Heroes


@app.post("/heroes/", response_model=HeroRead)
def create_hero(session: DBSession, hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroRead])
def read_heroes(
    session: DBSession, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    return session.exec(select(Hero).offset(offset).limit(limit)).all()


@app.get("/heroes/{hero_id}", response_model=HeroReadWithTeam)
def read_hero(session: DBSession, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(session: DBSession, hero_id: int, hero_update: HeroUpdate):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hero not found")

    hero_update_dict = hero_update.dict(exclude_unset=True)
    for key, value in hero_update_dict.items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)

    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(session: DBSession, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"ok": True}


# Path operations for Teams


@app.post("/teams/", response_model=TeamRead)
def create_team(session: DBSession, team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=list[TeamRead])
def read_teams(
    session: DBSession, offset: int = 0, limit: Annotated[int, Query(le=100)] = 0
):
    return session.exec(select(Team).offset(offset).limit(limit)).all()


@app.get("/teams/{team_id}/", response_model=TeamReadWithHeroes)
def read_team(session: DBSession, team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@app.patch("/teams/{team_id}/", response_model=TeamRead)
def update_team(session: DBSession, team_id: int, team: TeamUpdate):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    for key, value in team.dict(exclude_unset=True):
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team
