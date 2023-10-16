from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .teams import Team, TeamRead


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
