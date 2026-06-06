from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.models import Prediction, Match
from app.schemas import schemas
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.PredictionOut)
def create_prediction(prediction_in: schemas.PredictionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # 1. Check if match exists
    match = db.query(Match).filter(Match.id == prediction_in.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # 2. Prediction Lock: Check if match has started (match_date is UTC)
    if datetime.utcnow() >= match.match_date:
        raise HTTPException(status_code=400, detail="Predictions are locked for this match")
    
    # 3. Check if user already predicted for this match
    existing = db.query(Prediction).filter(
        Prediction.user_id == current_user.id, 
        Prediction.match_id == prediction_in.match_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Prediction already exists for this match")
    
    db_prediction = Prediction(
        **prediction_in.dict(),
        user_id=current_user.id
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

@router.patch("/{match_id}", response_model=schemas.PredictionOut)
def update_prediction(match_id: int, prediction_in: schemas.PredictionUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # 1. Check if match exists and is not locked
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if datetime.utcnow() >= match.match_date:
        raise HTTPException(status_code=400, detail="Predictions are locked for this match")
    
    # 2. Find the user's prediction for this match
    db_prediction = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.match_id == match_id
    ).first()
    
    if not db_prediction:
        raise HTTPException(status_code=404, detail="No prediction found for this match")
    
    # 3. Update fields
    for var, value in prediction_in.dict(exclude_unset=True).items():
        setattr(db_prediction, var, value)
    
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

@router.get("/me", response_model=List[schemas.PredictionOut])
def get_my_predictions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Prediction).filter(Prediction.user_id == current_user.id).all()

@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    from app.models.models import User
    results = db.query(
        User.username, 
        func.sum(Prediction.points_earned).label("total_points")
    ).join(Prediction).group_by(User.id).order_by(func.sum(Prediction.points_earned).desc()).all()
    
    return [{"username": r[0], "total_points": r[1] or 0} for r in results]
