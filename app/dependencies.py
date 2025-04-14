# dependency or dependable is just a function that can take the same parameters a path operatino
# function takes


# you can think of the dependable as a path operatino function
# without the decorator
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


# we are goig to rewrite the dependable above as a class
# dependables must be callable, and functions and classes and methods and instance that define the __call__ are callables
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


# here the dependencies has a yield
# the yielded value is what is returned to path operation function
# the part after the yield is executed after creating the response but before sending it
async def get_db():
    db = None # DBSession()
    try:
        yield db
    finally:
        db.close()