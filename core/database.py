from sqlmodel import Session, SQLModel, create_engine
from core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def create_db_and_tables():
    # Lazy-import models so SQLModel metadata registers User and Item
    from models.user import User
    from models.item import Item
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
