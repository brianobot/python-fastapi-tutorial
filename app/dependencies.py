# dependency or dependable is just a function that can take the same parameters a path operatino
# function takes


# you can think of the dependable as a path operatino function
# without the decorator
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
