from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from dotenv import dotenv_values
from contextlib import asynccontextmanager

from web_mission.routes import router as order_router
from web_mission.models import UserModel, ProductModel, Address

# from pydantic import BaseModel, Field
# from bson import ObjectId
# from typing import List, Optional

# MongoDB connection
config = dotenv_values(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"] + "test"]
    
    await create_user(app.database["user"])
    await create_product(app.database["product"])
    
    yield
    app.mongodb_client.close()
    await app.database.drop_collection("order")
    await app.database.drop_collection("product")
    await app.database.drop_collection("user")

app = FastAPI(lifespan=lifespan)
app.include_router(order_router, tags=["orders"], prefix="/orders")



# Fake user product
async def create_product(db):
    product = ProductModel(
        name="Oishi",
        description="Oishi bung no vi cay",
        price=12.0,
        stock=100
    )
    product = product.model_dump(by_alias=True)
    await db.insert_one(product)
    
    product = ProductModel(
        name="Keo sua Milkita",
        description="Keo sua Milkita duoc lam tu sua",
        price=25.0,
        stock=70
    )
    product = product.model_dump(by_alias=True)
    await db.insert_one(product)



async def create_user(db):
    address = Address(street="Main street", city="Example city")
    user = UserModel(
        name="John Weekend",
        password="securepassword123",
        phone="1234567890",
        address=address
    )

    user = user.model_dump(by_alias=True)
    await db.insert_one(user)


