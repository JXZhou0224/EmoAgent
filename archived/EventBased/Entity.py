from PlotGraph import Event, Timeline   
from pydantic import BaseModel, Field

class Entity(BaseModel):
    '''
    an object that can update with time
    need to link with a timeline 
    '''
    name: str = Field()

    

class Context(Entity):
    name: str = Field(default="context")
    

class Character(Entity):
    alias: list[str] = Field(default_factory=list)