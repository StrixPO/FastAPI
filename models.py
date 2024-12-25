from enum import Enum
from pydantic import BaseModel, validator
from datetime import date
from sqlmodel import SQLModel, Field, Relationship




class SauceURLChoices(str, Enum):
    TANGY = 'tangy'
    CREAMY = 'creamy'
    SPICY = 'spicy'
    SAVOURY = 'savoury'

class SauceChoices(str, Enum):
    TANGY = 'Tangy'
    CREAMY = 'Creamy'
    SPICY = 'Spicy'
    SAVOURY = 'Savoury'

class SidersBase(SQLModel):
    title:str
    release_date: date
    menu_id: int = Field(foreign_key="menu.id")

class Siders(SidersBase, table=True):
    id: int = Field(default = None, primary_key=True)
    menu: "Menu" = Relationship(back_populates ="siders")

class MenuBase(SQLModel):
    name: str
    sauce: SauceChoices

class MenuCreate(MenuBase):
    siders: list[SidersBase] | None = None

    @validator('sauce', pre=True)
    def title_case_genre(cls, value):
        return value.title()


class MenuWithID(MenuBase):
    id: int

class Menu(MenuBase, table =True):
    id: int = Field(default=None, primary_key=True)
    siders: list[Siders] = Relationship(back_populates="menu")
    date_formed: date | None = None