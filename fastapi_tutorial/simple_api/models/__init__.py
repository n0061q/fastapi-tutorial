"""
Update ForwardRefs for affected models

I wonder why this is not done automatically in SQLModel...

See: https://github.com/tiangolo/fastapi/issues/5607
"""


from .teams import TeamReadWithHeroes, TeamRead
from .heroes import HeroReadWithTeam, HeroRead


refs = {m.__name__: m for m in (TeamRead, HeroRead)}


def update_forward_refs():
    for model in TeamReadWithHeroes, HeroReadWithTeam:
        model.update_forward_refs(**refs)
