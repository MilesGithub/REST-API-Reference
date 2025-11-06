from typing import Optional
from pydantic import BaseModel, conint
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    is_admin: bool

class DrugCreate(BaseModel):
    name: str
    description: Optional[str] = None
    atc_code: Optional[str] = None
    indication: Optional[str] = None
    price_cents: conint(ge=0) = 0
    in_stock: conint(ge=0) = 0

class DrugRead(DrugCreate):
    id: int

class TrialCreate(BaseModel):
    title: str
    phase: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    drug_id: Optional[int] = None

class TrialRead(TrialCreate):
    id: int

class OrderCreate(BaseModel):
    drug_id: int
    quantity: conint(gt=0) = 1

class OrderRead(OrderCreate):
    id: int
    user_id: Optional[int]
    status: str
