from typing import Annotated

from sqlmodel import select
from fastapi import FastAPI, HTTPException, status, Query

from . import database
from . import models
from .models.heroes import HeroRead, HeroCreate, HeroUpdate, HeroReadWithTeam, Hero
from .models.teams import TeamRead, TeamCreate, TeamUpdate, TeamReadWithHeroes, Team


app = FastAPI()

models.update_forward_refs()


@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()


# /heroes/


@app.post("/heroes/", response_model=HeroRead)
def create_hero(session: database.DBSession, hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroRead])
def read_heroes(
    session: database.DBSession, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    return session.exec(select(Hero).offset(offset).limit(limit)).all()


@app.get("/heroes/{hero_id}", response_model=HeroReadWithTeam)
def read_hero(session: database.DBSession, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(session: database.DBSession, hero_id: int, hero_update: HeroUpdate):
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
def delete_hero(session: database.DBSession, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"ok": True}


# /teams/


@app.post("/teams/", response_model=TeamRead)
def create_team(session: database.DBSession, team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=list[TeamRead])
def read_teams(
    session: database.DBSession, offset: int = 0, limit: Annotated[int, Query(le=100)] = 0
):
    return session.exec(select(Team).offset(offset).limit(limit)).all()


@app.get("/teams/{team_id}/", response_model=TeamReadWithHeroes)
def read_team(session: database.DBSession, team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@app.patch("/teams/{team_id}/", response_model=TeamRead)
def update_team(session: database.DBSession, team_id: int, team: TeamUpdate):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    for key, value in team.dict(exclude_unset=True):
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team
