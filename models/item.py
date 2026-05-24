from typing import Annotated
from sqlmodel import Field, SQLModel


class ItemCreate(SQLModel):
    model_config = {"extra": "forbid"}

    name: Annotated[str, Field(max_length=100, min_length=5)]
    description: str | None = None
    price: float
    tax: float | None = None


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
