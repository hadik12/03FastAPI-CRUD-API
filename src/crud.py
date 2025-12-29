from typing import List, Optional

from sqlalchemy.orm import Session

from src import models, schemas


def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        in_stock=item.in_stock,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(
    db: Session,
    limit: int,
    offset: int,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    q: Optional[str] = None,
) -> List[models.Item]:
    query = db.query(models.Item)

    if min_price is not None:
        query = query.filter(models.Item.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Item.price <= max_price)
    if q:
        query = query.filter(models.Item.name.ilike(f"%{q}%"))

    return query.order_by(models.Item.created_at.desc()).offset(offset).limit(limit).all()


def update_item(db: Session, db_item: models.Item, item: schemas.ItemUpdate) -> models.Item:
    for field, value in item.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, db_item: models.Item) -> None:
    db.delete(db_item)
    db.commit()
