from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Match
from app.schemas import schemas
from app.api.deps import get_admin_user
from app.services.scoring import calculate_match_points

router = APIRouter()

@router.get("/", response_model=List[schemas.MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()

@router.post("/", response_model=schemas.MatchOut)
def create_match(match_in: schemas.MatchCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_match = Match(**match_in.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

@router.patch("/{match_id}", response_model=schemas.MatchOut)
def update_match(match_id: int, match_in: schemas.MatchUpdate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    for var, value in match_in.dict(exclude_unset=True).items():
        setattr(db_match, var, value)
    
    db.commit()
    db.refresh(db_match)
    
    # Trigger scoring engine if status becomes 'finished'
    if db_match.status == "finished":
        calculate_match_points(db, match_id)
        
    return db_match
