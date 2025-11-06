from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlmodel import Session
from . import crud
from .models import Drug, ClinicalTrial, Order
from .schemas import (DrugCreate, DrugRead, TrialCreate, TrialRead, OrderCreate, OrderRead, Token, UserCreate, UserRead)
from .auth import get_password_hash, verify_password, create_access_token, get_current_active_user, get_current_admin_user

app = FastAPI(title="Pharma REST API")

@app.on_event("startup")
def on_startup():
    crud.init_db()
    # seed demo data
    try:
        import app.initial_data as seedmod
        seedmod.seed()
    except Exception:
        pass

# Auth: token endpoint
@app.post('/auth/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# User creation (admin only)
@app.post('/users', response_model=UserRead)
def create_user_endpoint(user_in: UserCreate, current_user=Depends(get_current_admin_user)):
    hashed = get_password_hash(user_in.password)
    user = crud.create_user(user_in.username, hashed, is_admin=False)
    return UserRead(id=user.id, username=user.username, is_admin=user.is_admin)

# Drugs
@app.post('/drugs', response_model=DrugRead)
def create_drug_endpoint(drug_in: DrugCreate, current_user=Depends(get_current_admin_user)):
    drug = Drug(**drug_in.dict())
    created = crud.create_drug(drug)
    return DrugRead(id=created.id, **drug_in.dict())

@app.get('/drugs', response_model=List[DrugRead])
def list_drugs_endpoint(skip: int = 0, limit: int = 100):
    drugs = crud.list_drugs(skip=skip, limit=limit)
    return [DrugRead(id=d.id, name=d.name, description=d.description, atc_code=d.atc_code, indication=d.indication, price_cents=d.price_cents, in_stock=d.in_stock) for d in drugs]

@app.get('/drugs/{drug_id}', response_model=DrugRead)
def get_drug_endpoint(drug_id: int):
    drug = crud.get_drug(drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return DrugRead(id=drug.id, name=drug.name, description=drug.description, atc_code=drug.atc_code, indication=drug.indication, price_cents=drug.price_cents, in_stock=drug.in_stock)

# Clinical trials
@app.post('/trials', response_model=TrialRead)
def create_trial_endpoint(trial_in: TrialCreate, current_user=Depends(get_current_admin_user)):
    trial = ClinicalTrial(**trial_in.dict())
    created = crud.create_trial(trial)
    return TrialRead(id=created.id, **trial_in.dict())

@app.get('/trials', response_model=List[TrialRead])
def list_trials_endpoint(skip: int = 0, limit: int = 100):
    trials = crud.list_trials(skip=skip, limit=limit)
    return [TrialRead(id=t.id, title=t.title, phase=t.phase, start_date=t.start_date, end_date=t.end_date, drug_id=t.drug_id) for t in trials]

# Orders (auth required)
@app.post('/orders', response_model=OrderRead)
def create_order_endpoint(order_in: OrderCreate, current_user=Depends(get_current_active_user)):
    # check stock
    drug = crud.get_drug(order_in.drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    if drug.in_stock < order_in.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    order = Order(user_id=current_user.id, drug_id=order_in.drug_id, quantity=order_in.quantity)
    created = crud.create_order(order)
    crud.adjust_inventory(drug.id, -order_in.quantity)
    return OrderRead(id=created.id, drug_id=created.drug_id, quantity=created.quantity, user_id=created.user_id, status=created.status)

# Health check
@app.get('/health')
def health():
    return {"status": "ok"}
