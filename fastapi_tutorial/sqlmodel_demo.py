from sqlmodel import Session, create_engine, SQLModel, Field, select


engine = create_engine("sqlite:///database.db", echo=True)


class Hero(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    secret_name: str
    age: int | None = None


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Moroz", secret_name="Krasny Nos", age=100)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    def print_heroes(title):
        print(title)
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)

    print_heroes("Before interacting with the database")

    with Session(engine) as s:
        s.add(hero_1)
        s.add(hero_2)
        s.add(hero_3)

        print_heroes("After adding to the session")

        s.commit()

        s.refresh(hero_1)
        s.refresh(hero_2)
        # s.refresh(hero_3)

        print_heroes("After committing the session")

    print_heroes("After the session is closed")


def select_heroes():
    with Session(engine) as s:
        results = s.exec(select(Hero)).all()
        # for h in results:
        #     print(h)
        print(f"Heroes in total: {len(results)}")


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
