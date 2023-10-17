import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from . import main
from . import database
from .models.heroes import Hero


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def client(db_session: Session):
    main.app.dependency_overrides[database.get_db_session] = lambda: db_session
    yield TestClient(main.app)
    main.app.dependency_overrides.clear()


def test_create_hero(client: TestClient):
    response = client.post("/heroes/", json={"name": "John", "secret_name": "Jack"})

    assert response.status_code == 200
    data = response.json()
    print(data)

    assert data["name"] == "John"
    assert data["secret_name"] == "Jack"
    assert data["age"] == None
    assert data["id"] != None


def test_create_hero_incomplete(client: TestClient):
    response = client.post("/heroes/", json={"name": "John"})
    assert response.status_code == 422


def test_create_hero_invalid(client: TestClient):
    response = client.post("/heroes/", json={"name": "John", "secret_name": None})
    assert response.status_code == 422


def test_read_heroes(client: TestClient, db_session: Session):
    hero_1 = Hero(name='Hero1', secret_name='secret1')
    hero_2 = Hero(name='Hero2', secret_name='secret2')
    db_session.add(hero_1)
    db_session.add(hero_2)
    db_session.commit()

    response = client.get("/heroes/")
    assert response.status_code == 200

    expected = [h.dict() for h in (hero_1, hero_2)]
    assert response.json() == expected


def test_read_hero(client: TestClient, db_session: Session):
    hero = Hero(name='Hercules', secret_name='Mighty One')
    db_session.add(hero)
    db_session.commit()

    response = client.get(f"/heroes/{hero.id}")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == hero.name
    assert data['secret_name'] == hero.secret_name
    assert data['id'] == hero.id
    assert data['age'] == hero.age

