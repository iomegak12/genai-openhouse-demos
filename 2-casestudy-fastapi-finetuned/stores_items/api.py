import time
import asyncio

from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from stores_items.common import Base, engine, get_db
from stores_items.items import ItemRepo, Item, ItemCreate
from stores_items.stores import StoreRepo, Store, StoreCreate

app = FastAPI(
    title="Stores and Items API",
    description="Simple FastAPI REST Service for Stores and Items",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validate_exception_handler(request, error):
    base_error_message = f"Failed to Execute : {request.method}: {request.url}"

    return JSONResponse(
        status_code=400,
        content={
            "message": f"{base_error_message}, Detail: {error}"
        }
    )


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print("Inside the Middleware ...")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:0.4f} second(s)")

    return response


@app.post("/",
          tags=["Item"],
          response_model=Item,
          status_code=201)
async def create_item(item_request: ItemCreate, db: Session = Depends(get_db)):
    """
    Create an Item and Store it in the database
    """

    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)

    if db_item:
        raise HTTPException(
            status_code=400,
            detail="Item Already Exists!"
        )

    return await ItemRepo.create(db=db, item=item_request)


@app.get("/items",
         tags=["Item"],
         response_model=List[Item])
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the items stored in the database,
    Optionally specify the Name of the Item
    """

    if name:
        items = []
        db_item = ItemRepo.fetch_by_name(db, name)
        items.append(db_item)
    else:
        return ItemRepo.fetch_all(db)


@app.get("/items/{item_id}",
         tags=["Item"],
         response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the item with the given ID by the User, that stored from the database
    """

    db_item = ItemRepo.fetch_by_id(db, item_id)

    if db_item is None:
        raise HTTPException(
            status_code=404,
            detail="Item Not Found with the Given ID")

    return db_item


@app.post("/stores",
          tags=["Store"],
          response_model=Store,
          status_code=201)
async def create_store(store_request: StoreCreate, db: Session = Depends(get_db)):
    """
    Create a Store and save it in the database
    """

    db_store = StoreRepo.fetch_by_name(db, name=store_request.name)

    print(db_store)

    if db_store:
        raise HTTPException(
            status_code=400,
            detail="Store Already Exists!"
        )

    return await StoreRepo.create(db=db, store=store_request)


@app.get("/stores",
         tags=["Store"],
         response_model=List[Store])
def get_all_stores(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the stores stored in the database!
    """
   
    stores = []

    if name:
        db_store = StoreRepo.fetch_by_name(db, name)
        print(db_store)
        stores.append(db_store)
    else:
        stores = StoreRepo.fetch_all(db)

    return stores


@app.get("/stores/{store_id}",
         tags=["Store"],
         response_model=Store)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """
    Get the store details with the given Store ID
    """
   
    db_store = StoreRepo.fetch_by_id(db, store_id)

    if db_store is None:
        raise HTTPException(
            status_code=401,
            detail="Store Not Found with the Given Store ID"
        )

    return db_store
