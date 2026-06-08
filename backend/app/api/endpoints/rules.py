from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import ScoringRule, PhaseMultiplier
from app.schemas import schemas
from app.api.deps import get_admin_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ScoringRuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(ScoringRule).all()

@router.post("/", response_model=schemas.ScoringRuleOut)
def create_rule(rule_in: schemas.ScoringRuleCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    # Only one active rule at a time
    if rule_in.is_active:
        db.query(ScoringRule).filter(ScoringRule.is_active == True).update({"is_active": False})
    
    db_rule = ScoringRule(**rule_in.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.patch("/{rule_id}", response_model=schemas.ScoringRuleOut)
def update_rule(rule_id: int, rule_in: schemas.ScoringRuleCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_rule = db.query(ScoringRule).filter(ScoringRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    if rule_in.is_active:
        db.query(ScoringRule).filter(ScoringRule.is_active == True).update({"is_active": False})

    for var, value in rule_in.dict().items():
        setattr(db_rule, var, value)
    
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/multipliers", response_model=List[schemas.PhaseMultiplierOut])
def list_multipliers(db: Session = Depends(get_db)):
    return db.query(PhaseMultiplier).all()

@router.patch("/multipliers/{pm_id}", response_model=schemas.PhaseMultiplierOut)
def update_multiplier(pm_id: int, pm_in: schemas.PhaseMultiplierCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_pm = db.query(PhaseMultiplier).filter(PhaseMultiplier.id == pm_id).first()
    if not db_pm:
        raise HTTPException(status_code=404, detail="Multiplier not found")
    
    for var, value in pm_in.dict().items():
        setattr(db_pm, var, value)
    
    db.commit()
    db.refresh(db_pm)
    return db_pm
