import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from bson import ObjectId
from bson.errors import InvalidId
import logging

load_dotenv()  # Load environment variables

PARKING_LOT_SIZE = int(os.getenv("PARKING_LOT_SIZE", 10))
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "parking_lot_db")

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Pydantic models for request and response
class Car(BaseModel):
    car_number: str


class Slot(BaseModel):
    slot_number: str


class ParkedCar(BaseModel):
    car_number: str
    slot: str


# Database Dependency
def get_db_client():
    db_client = AsyncIOMotorClient(MONGODB_URL)
    try:
        yield db_client[MONGODB_DBNAME]
    finally:
        db_client.close()


@app.post("/park", response_model=ParkedCar)
async def park_car(car: Car, db=Depends(get_db_client)):
    parked_cars_collection = db.parked_cars
    existing_car = await parked_cars_collection.find_one({"car_number": car.car_number})

    if existing_car:
        raise HTTPException(status_code=400, detail="Car is already parked.")

    total_parked_cars = await parked_cars_collection.count_documents({})

    if total_parked_cars >= PARKING_LOT_SIZE:
        raise HTTPException(status_code=400, detail="Parking lot is full.")

    result = await parked_cars_collection.insert_one({"car_number": car.car_number})
    parked_car = await parked_cars_collection.find_one({"_id": result.inserted_id})

    return {"car_number": parked_car["car_number"], "slot": str(parked_car["_id"])}


@app.post("/unpark")
async def unpark_car(slot: Slot, db=Depends(get_db_client)):
    parked_cars_collection = db.parked_cars

    try:
        obj_id = ObjectId(slot.slot_number)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid slot number format.")

    result = await parked_cars_collection.find_one_and_delete({"_id": obj_id})

    if not result:
        raise HTTPException(status_code=404, detail="Slot not found or already empty.")

    return {"message": "Car removed from slot successfully."}


@app.get("/info/{identifier}", response_model=ParkedCar)
async def get_info(identifier: str, db=Depends(get_db_client)):
    parked_cars_collection = db.parked_cars

    try:
        obj_id = ObjectId(identifier)
        car_info = await parked_cars_collection.find_one({"_id": obj_id})
    except InvalidId:
        car_info = await parked_cars_collection.find_one({"car_number": identifier})

    if not car_info:
        raise HTTPException(status_code=404, detail="Car or slot not found.")

    return {"car_number": car_info["car_number"], "slot": str(car_info["_id"])}
