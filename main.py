from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    text: str = None
    is_done: bool = False

 
items: list[str] = []


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.post("/items/", response_model=Item)
# functions arguments are expected a query parameter in the url for the route
# if the function argument is a instance of BaseModel, the item is expected as a JSON payload instead
def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items/", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}")
# if the function argument is available in the path, the argument is expected to be a path variable
def get_item(item_id: int):
    if item_id < len(items) and item_id > 0:
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.patch("/items/{item_id}", status_code=202)
def update_item(item_id: int, item: Item):
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