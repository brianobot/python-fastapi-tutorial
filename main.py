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


@app.post("/items/", response_model=Item)
# functions arguments are expected a query parameter in the url for the route
# if the function argument is a instance of BaseModel, the item is expected as a JSON payload instead
async def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items/", response_model=list[Item])
async def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}")
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
