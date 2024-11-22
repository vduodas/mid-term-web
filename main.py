from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from dotenv import dotenv_values
# from contextlib import asynccontextmanager

# from pymongo import MongoClient
from web_mission.routes import router as order_router
from web_mission.models import UserModel, ProductModel, Address

# from pydantic import BaseModel, Field
# from bson import ObjectId
# from typing import List, Optional

config = dotenv_values(".env")

app = FastAPI()

# MongoDB connection
app.mongo_client = AsyncIOMotorClient(config["ATLAS_URI"])
app.database = app.mongo_client[config["DB_NAME"]]


# Fake user product
async def create_product(db):
    product = ProductModel(
        name="Oishi",
        description="Oishi bung no vi cay",
        price=12.0,
        stock=100
    )
    product = product.model_dump(by_alias=True)
    await db["product"].insert_one(product)
    
    product = ProductModel(
        name="Keo sua Milkita",
        description="Keo sua Milkita duoc lam tu sua",
        price=25.0,
        stock=70
    )
    product = product.model_dump(by_alias=True)
    await db["product"].insert_one(product)



async def create_user(db):
    address = Address(street="Main street", city="Example city")
    user = UserModel(
        name="John Weekend",
        password="securepassword123",
        phone="1234567890",
        address=address
    )

    user = user.model_dump(by_alias=True)
    await db["user"].insert_one(user)


# Sample data insertion should be awaited
@app.on_event("startup")
async def startup_event():
    await create_user(app.database)
    await create_product(app.database)

# Include order router
app.include_router(order_router, tags=["orders"], prefix="/orders")

# MongoDB shutdown
@app.on_event("shutdown")
def shutdown_event():
    app.mongo_client.close()
