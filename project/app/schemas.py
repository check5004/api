from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class CustomerBase(BaseModel):
    name: str
    phone_number: str
    birth_date: date

class CustomerCreate(CustomerBase):
    id: Optional[int] = None
    delete_flag: bool = Field(default=False)

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True
