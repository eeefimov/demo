# pylint: disable=invalid-name
"""User models"""
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class User:
    """User values model"""
    name: str
    email: str
    password: str


@dataclass
class Register:
    """Register values model"""
    email: str
    name: str


@dataclass
class RegisterModel:
    """Register response model"""
    success: bool
    user: dict[Register]
    accessToken: str
    refreshToken: str


# @dataclass
class MsgModel(BaseModel):
    """Different message response model"""
    success: bool
    message: str


@dataclass
class UserModel:
    """User response model"""
    success: bool
    user: dict[Register]
