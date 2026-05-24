from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated

import urllib.parse

escaped_password = urllib.parse.quote_plus("tarun@123")
DATABASE_URL = f"mysql+pymysql://root:{escaped_password}@localhost/fastapi"
print(DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    echo=True
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# Request schema
class ItemCreate(SQLModel):
    model_config = {"extra": "forbid"}

    name: Annotated[str, Field(max_length=100 ,min_length=5)]
    description: str | None = None
    price: float
    tax: float | None = None


# DB model
class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/", response_model=Item)
def create_item(
    item: ItemCreate,
    session: Session = Depends(get_session)
):
    db_item = Item.model_validate(item)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@app.get("/items/{item_id}", response_model=Item)
def read_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item