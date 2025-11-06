from sqlmodel import Session, select, SQLModel, create_engine
from typing import List, Optional
from .models import User, Drug, ClinicalTrial, Order

engine = create_engine("sqlite:///./pharma.db", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

# Users
def create_user(username: str, hashed_password: str, is_admin: bool = False) -> User:
    with Session(engine) as session:
        user = User(username=username, hashed_password=hashed_password, is_admin=is_admin)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_username(username: str) -> Optional[User]:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        result = session.exec(statement).first()
        return result

# Drugs
def create_drug(drug: Drug) -> Drug:
    with Session(engine) as session:
        session.add(drug)
        session.commit()
        session.refresh(drug)
        return drug

def list_drugs(skip: int = 0, limit: int = 100) -> List[Drug]:
    with Session(engine) as session:
        statement = select(Drug).offset(skip).limit(limit)
        return session.exec(statement).all()

def get_drug(drug_id: int) -> Optional[Drug]:
    with Session(engine) as session:
        return session.get(Drug, drug_id)

# Trials
def create_trial(trial: ClinicalTrial) -> ClinicalTrial:
    with Session(engine) as session:
        session.add(trial)
        session.commit()
        session.refresh(trial)
        return trial

def list_trials(skip: int = 0, limit: int = 100) -> List[ClinicalTrial]:
    with Session(engine) as session:
        statement = select(ClinicalTrial).offset(skip).limit(limit)
        return session.exec(statement).all()

# Orders
def create_order(order: Order) -> Order:
    with Session(engine) as session:
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

# update inventory
def adjust_inventory(drug_id: int, delta: int) -> Optional[Drug]:
    with Session(engine) as session:
        drug = session.get(Drug, drug_id)
        if not drug:
            return None
        drug.in_stock = max(0, drug.in_stock + delta)
        session.add(drug)
        session.commit()
        session.refresh(drug)
        return drug
