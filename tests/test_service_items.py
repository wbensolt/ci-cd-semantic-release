import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item_service import ItemService


# ------------------------------
# Fixtures
# ------------------------------
@pytest.fixture
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture
def session(engine: Session):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def sample_item_data():
    return ItemCreate(name="Test Item", description="A test item", price=10.0)


# ------------------------------
# Tests ItemService
# ------------------------------
def test_create_item(session: Session, sample_item_data: ItemCreate):
    item = ItemService.create(session, sample_item_data)
    assert item.id is not None
    assert item.name == sample_item_data.name

def test_get_all_items(session: Session, sample_item_data: ItemCreate):
    ItemService.create(session, sample_item_data)
    items = ItemService.get_all(session, skip=0, limit=10)
    assert len(items) == 1

def test_get_by_id(session: Session, sample_item_data: ItemCreate):
    item = ItemService.create(session, sample_item_data)
    fetched = ItemService.get_by_id(session, item.id)
    assert fetched.id == item.id

def test_update_item(session: Session, sample_item_data: ItemCreate):
    item = ItemService.create(session, sample_item_data)
    update_data = ItemUpdate(name="Updated Item")
    updated = ItemService.update(session, item.id, update_data)
    assert updated.name == "Updated Item"

def test_delete_item(session: Session, sample_item_data: ItemCreate):
    item = ItemService.create(session, sample_item_data)
    result = ItemService.delete(session, item.id)
    assert result is True
    assert ItemService.get_by_id(session, item.id) is None

def test_delete_nonexistent_item(session: Session):
    result = ItemService.delete(session, 999)
    assert result is False
