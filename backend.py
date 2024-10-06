#uvicorn backend:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import time

# FastAPI instance
app = FastAPI()

# Pydantic model to define an order structure
class Order(BaseModel):
    id: int
    name: str
    contact: str
    plate: str
    available_hour: time

# In-memory database (for simplicity, you can later switch to a real DB)
orders_db: List[Order] = []

# Endpoint to add a new order
@app.post("/orders/")
def add_order(order: Order):
    orders_db.append(order)
    return {"message": "Order added successfully!", "order": order}

# Endpoint to view all orders
@app.get("/orders/")
def view_orders():
    return orders_db
