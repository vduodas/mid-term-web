from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from web_mission.models import UserModel, ProductModel, OrderModel, OrderItem

router = APIRouter()

# Lấy tất cả thông tin liên quan đến sản phẩm theo product_id
@router.get("/", response_description="List all products", response_model=List[ProductModel])
async def list_products(request: Request):
    products = await request.app.database["product"].find(limit=100).to_list(length=100)
    if products:
        return products
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unavailable products")


@router.post("/", response_description="Create a new order", status_code=status.HTTP_201_CREATED, response_model=OrderModel)
async def create_order(request: Request, order : OrderModel = Body(...)):
    order_data = jsonable_encoder(order)

    ########### total_price
    # Insert new order into the "order" collection
    result = await request.app.database["order"].insert_one(order_data)
    
    # Fetch the created order back from the database
    new_order = await request.app.database["order"].find_one({"_id": result.inserted_id})
    
    return new_order

    
    
@router.delete("/{id}", response_description="Cancel order by order_id")
async def delete_order(id: str, request: Request, response = Response):
    delete_result = await request.app.database["order"].delete_one({"order_id": id})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} has not been created yet")



@router.put("/", response_description="Change order's information by product_id", response_model=OrderModel)
async def update_order(request: Request, uid: str, orders: List[OrderItem]):
    # Find the specific order by product_id 
    order_to_update = await request.app.database["order"].find_one({"user_id": uid})

    if not order_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No order found with user_id {uid}")

    # Update the order in the database
    await request.app.database["order"].update_one(
        {"user_id": uid}, 
        {"$set": {"orders": orders}}
    )
    
    # Fetch the updated order
    updated_order = await request.app.database["order"].find_one({"user_id": uid})
    
    return updated_order

    
    