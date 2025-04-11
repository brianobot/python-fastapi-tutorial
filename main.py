from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Brian's FastAPI API",
    summary="This is a short summary of the api",
    description="THis is a decsription of what the api is meant for",
    version="0.2.0",
)


class Item(BaseModel):
    text: str = None
    is_done: bool = False


items: list[str] = []

# when defining paths order matter
# /users/me being a fixed path should come before /users/{username} being a variable path
# cause /users/me would always match for /users/{username}


@app.get("/")  # this is a path operation decorator, this is for the root path '/'
# and the operation supported is GET http method
async def read_root():
    # the return values can be a list, tuple, dict, set, str, int, float
    # you can also return Pydantic models, or a sequence of it
    return {"hello": "world"}


@app.get("/ages")
async def read_ages():
    return {3.123, 23.45, 232.53, 23}


@app.get("/prices")
async def read_prices():
    return [
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
    ]


# in this case below we can only have a fixed number of predefined stock
# so we use enums to restrict the options

from enum import Enum
from random import random


class Stock(str, Enum):
    ngn = "ngn"
    eur = "eur"
    usd = "usd"


@app.get("/{stock_name}/prices")
async def stock_prices(stock_name: Stock):
    return {"name": stock_name, "prices": [random() for _ in range(12)]}


@app.post("/items/", response_model=Item)
# functions arguments are expected a query parameter in the url for the route
# if the function argument is a instance of BaseModel, the item is expected as a JSON payload instead
async def create_item(item: Item):
    items.append(item)
    return item


class User(BaseModel):
    email: str
    first_name: str
    last_name: str


from fastapi import Query, Path, Cookie, Header
from typing import Annotated


@app.post("/users")
# additional validation can be applied on query parameters with the Query and Annotated class
# the case below means that user_type is an optional string that but must be less than 51 characters when 
# provided
# there are similar class like Query, Query here is used because the type in question is a query
# there is Cookie, Path, Body, Header, Form File that also accept the same arguments as Query
# you can have more validation like min_length, pattern for regex, title, description, alias, deprecated  etc
# Technical Note: Query, Path are all functions that when called create instance of classes with the same name
async def users(user: User, user_type: Annotated[str | None, Query(max_length=50)] = None):
    return user


@app.get("/items/", response_model=list[Item])
async def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}") # a path parameter is always required, even if it's set to None in the function signtature
# if the function argument is available in the path, the argument is expected to be a path variable
# path parameters must be passed to the function as a function argument
async def get_item(item_id: int):
    if item_id < len(items) and item_id > 0:
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.patch("/items/{item_id}", status_code=202)
async def update_item(item_id: int, item: Item):
    if item_id < len(items) and item_id > 0:
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, item: Item):
    if item_id < len(items) and item_id > 0:
        del items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


from pydantic import Field
from typing import Literal


class FilterQuery(BaseModel):
    model_config = {"extra": "forbid"} # this forbids extra fields on the fields received

    # Field works the same way as Query, Body and Path, 
    # it has the same parameters
    limit: int = Field(100, gt=0, le=1000)
    # the Field can take an additional argument call examples that shows example of the field
    # this would be used for API docs, this applies to Query, Body and the likes 
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: set[str] = set()


@app.get("/products")
async def read_products(filter_query: Annotated[FilterQuery, Query()]):
    return filter_query