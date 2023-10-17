from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine


DB_FILE_NAME = "database.db"


engine = create_engine(
    f"sqlite:///{DB_FILE_NAME}", echo=True, connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_db_session)]
