from fastapi import FastAPI
from typing import List
from fastapi import Request

app = FastAPI(
    title="Main1.py",
    summary="Just checking",
    description=(
        "hello this i sthe main1.py running on uvicorn"
        " Next line many things to do"
        )
)

@app.get("/",
         tags=["there"])
def home():
    """Doc string to get to know about the function"""
    return {
        "home" : "hello you are at home",
        "orders" : {
            "item1" : "apple",
            "status" : "completed"
        },
        "Exit" : "Done"
    }

@app.get("/request",
         tags=["hello"])
async def req_func(req : Request):
    """Inspect the incoming request"""
    return{
        "headers" : dict(req.headers),
        "url" : str(req.url),
        "method" : req.method,
        "path_param" : str(req.path_params),
        "query_param" : str(req.query_params)
    }

#i can do more in decorator to define and document the decorator itself
@app.get(
    "/MoreInfo",
    summary="This is more about my request",
    description=(
        "Hello there"
        "Moe gello"
    ),
    deprecated=False,
    tags=["hello","there","request"]
)
async def Func(request : Request):
    """This is a new endpoiiiint"""
    return{
        "headers" : dict(request.headers),
        "url" : str(request.url),
     "method" : request.method,
        "path_param" : str(request.path_params),
        "query_param" : str(request.query_params)
    }