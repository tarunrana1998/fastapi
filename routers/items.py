from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from core.dependencies import get_current_user
from models.item import Item, ItemCreate
from models.user import User

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=Item)
def create_item(
    item: ItemCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session)
):
    db_item = Item.model_validate(item)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@router.get("/{item_id}", response_model=Item)
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
