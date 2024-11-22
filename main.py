from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from dotenv import dotenv_values
# from contextlib import asynccontextmanager

# from pymongo import MongoClient
from web_mission.routes import router as order_router
# from web_mission.models import UserModel, ProductModel, Address

# from pydantic import BaseModel, Field
# from bson import ObjectId
# from typing import List, Optional

config = dotenv_values(".env")

app = FastAPI()

# MongoDB connection
app.mongo_client = AsyncIOMotorClient(config["ATLAS_URI"])
app.database = app.mongo_client[config["DB_NAME"]]

# Include order router
app.include_router(order_router, tags=["orders"], prefix="/orders")


