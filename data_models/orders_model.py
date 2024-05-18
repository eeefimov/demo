"""Orders models"""
from typing import List
from pydantic import BaseModel, Field
from data_models.ingredients_models import Ingredient


class Order(BaseModel):
    """GET Order model"""
    ingredients: List[str]
    _id: str
    status: str
    name: str
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')
    number: int


class OrdersModel(BaseModel):
    """GET Order response model"""
    success: bool
    orders: List[Order]
    total: int
    total_today: int = Field(alias='totalToday')


class Owner(BaseModel):
    """POST Order owner model"""
    name: str
    email: str
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')


class OrderDetails(BaseModel):
    """POST Order ingredients model"""
    ingredients: List[Ingredient]
    _id: str
    owner: Owner
    status: str
    name: str
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')
    number: int
    price: int


class OrderResponse(BaseModel):
    """POST Order response model"""
    success: bool
    name: str
    order: OrderDetails
