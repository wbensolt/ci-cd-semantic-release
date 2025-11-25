from sqlmodel import Session, select
from typing import List, Optional

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:

    @staticmethod
    def get_all(db: Session, skip: int, limit: int) -> List[Item]:
        return db.exec(select(Item).offset(skip).limit(limit)).all()

    @staticmethod
    def get_by_id(db: Session, item_id: int) -> Optional[Item]:
        return db.get(Item, item_id)

    @staticmethod
    def create(db: Session, item_data: ItemCreate) -> Item:
        item = Item(**item_data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update(db: Session, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        item = db.get(Item, item_id)
        if not item:
            return None
        for key, value in item_data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, item_id: int) -> bool:
        item = db.get(Item, item_id)
        if not item:
            return False
        db.delete(item)
        db.commit()
        return True
