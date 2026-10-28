from fastapi import FastAPI

app = FastAPI(
    title="My First FastAPI App",
    description="This is a simple FastAPI application that demonstrates the basic functionality of FastAPI.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
def basic_func():
    return {"message" : "Hello there !"}