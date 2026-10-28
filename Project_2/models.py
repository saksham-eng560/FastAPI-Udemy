from pydantic import BaseModel

class PinCode(BaseModel):
    pincode: str
    city: str
    state: str
    country: str