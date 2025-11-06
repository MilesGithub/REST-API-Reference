from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    is_admin: bool = Field(default=False)

class Drug(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    atc_code: Optional[str] = None
    indication: Optional[str] = None
    price_cents: int = Field(default=0)
    in_stock: int = Field(default=0)

class ClinicalTrial(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    phase: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    drug_id: Optional[int] = Field(default=None, foreign_key="drug.id")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    drug_id: Optional[int] = Field(default=None, foreign_key="drug.id")
    quantity: int = Field(default=1)
    status: str = Field(default="pending")
