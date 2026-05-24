from typing import Annotated
from sqlmodel import SQLModel, Field,create_engine

from fastapi import Depends, FastAPI

app = FastAPI()

def create_db_and_tables():
    engine = create_engine("sqlite:///database.db")
    SQLModel.metadata.create_all(engine)


class Item(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/items/{item_id}")
async def read_items(item_id: int, skip: int = 0, limit: int = 10):
    response = {}
    if q:
        response.update({"q": q})

    items = fake_items_db[skip : skip + limit]
    response.update({"items": items})
    return response

@app.post("/items/")
async def create_item(item: Item):
    return item