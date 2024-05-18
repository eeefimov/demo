"""Ingredients models"""
from pydantic import BaseModel


def filter__v_field(func):
    """
    There is a key '__v' in actual response json.
    The __v field is an internal field commonly used in MongoDB
    to track document versions.
    It is automatically managed by MongoDB
    and typically not relevant to the application logic.

    Decorator and function down below exclude '__v' from
    response json data_models.
    In another way there is an error of reserved code '__v'.
    """
    def wrapper(response):
        for item in response['data']:
            item.pop('__v', None)
        return func(response)
    return wrapper


@filter__v_field
def get_data(response):
    """Serialise ingredients response."""
    return response


class Ingredient(BaseModel):
    """Base model for ingredients"""
    _id: str
    name: str
    type: str
    proteins: int
    fat: int
    carbohydrates: int
    calories: int
    price: int
    image: str
    image_mobile: str
    image_large: str


class IngredientsModel(BaseModel):
    """Base model for ingredients response"""
    success: bool
    data: list[Ingredient]
