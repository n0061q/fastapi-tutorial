from sqlmodel import Session, create_engine, SQLModel, Field, select, Relationship


engine = create_engine("sqlite:///database.db", echo=True)


class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, primary_key=True, foreign_key="team.id")
    hero_id: int | None = Field(default=None, primary_key=True, foreign_key="hero.id")


class Team(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    secret_name: str
    age: int | None = None

    teams: list["Team"] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes_with_teams():
    with Session(engine) as s:
        h1 = Hero(name="Caesar", secret_name="")

        t1 = Team(
            name="Fatherland",
            headquarters="Earth",
            heroes=[
                Hero(name="El Presidente", secret_name="VVP"),
                Hero(name="Prime Minister", secret_name="KGB"),
                h1,
            ],
        )
        t2 = Team(
            name="Zerg",
            headquarters="HQ",
            heroes=[Hero(name="Z1", secret_name="Shorty"), h1],
        )

        s.add(t1)
        s.add(t2)
        s.commit()

        for item in h1, t1, t2:
            s.refresh(item)

        print(f"{h1!r} --- {[t.name for t in h1.teams]}")
        print(f"{t1!r} --- {[h.name for h in t1.heroes]}")
        print(f"{t2!r} --- {[h.name for h in t2.heroes]}")


def update_heroes():
    with Session(engine) as s:
        z1 = s.exec(select(Hero).where(Hero.name == "Z1")).one()
        fatherland = s.exec(select(Team).where(Team.name == "Fatherland")).one()

        z1.teams = []
        fatherland.heroes.append(z1)

        s.add(fatherland)
        s.commit()


def main():
    create_db_and_tables()
    create_heroes_with_teams()
    update_heroes()


if __name__ == "__main__":
    main()
