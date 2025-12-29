import logging
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.auth import verify_api_key
from src.db import Base, engine, get_db
from src.settings import ensure_log_directory, get_settings

settings = get_settings()
ensure_log_directory(settings.log_file)

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.log_file),
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI CRUD API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()
@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}
@app.on_event("startup")
def on_startup() -> None:
    logger.info("Creating database tables if they do not exist")
    Base.metadata.create_all(bind=engine)


@app.post("/items", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    logger.info("Creating item '%s'", item.name)
    return crud.create_item(db, item)


@app.get("/items", response_model=List[schemas.ItemResponse])
def list_items(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    q: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    logger.info(
        "Listing items limit=%s offset=%s min_price=%s max_price=%s q=%s",
        limit,
        offset,
        min_price,
        max_price,
        q,
    )
    return crud.get_items(db, limit=limit, offset=offset, min_price=min_price, max_price=max_price, q=q)


@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    logger.info("Fetching item id=%s", item_id)
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    logger.info("Updating item id=%s", item_id)
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return crud.update_item(db, db_item, item)


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    logger.info("Deleting item id=%s", item_id)
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    crud.delete_item(db, db_item)
    return None
