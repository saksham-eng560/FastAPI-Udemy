from fastapi import FastAPI,HTTPException
from models import PinCode
from db import pincodes

app = FastAPI(
    title="PinCode API",
    description="This API provides access to a database of pin codes and their corresponding city, state, and country information.",
    version="1.0.69",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get(
    "/home/{pincode}",
    description="Pincode Finding Service",
    response_model=PinCode,
    deprecated=False
)
def func(pincode : str):
    if len(pincode) != 6:
        raise HTTPException(status_code=422,detail="Error Response")
    for pins in pincodes:
        if pins["pincode"] == pincode:
            return pins
    raise HTTPException(status_code=404,detail="NOT FOUND")

