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

@router.get("/match/{match_id}", response_model=List[schemas.MatchPredictionOut])
def get_match_predictions(match_id: int, db: Session = Depends(get_db)):
    from app.models.models import User
    
    # Join Prediction with User to get usernames
    predictions = db.query(Prediction, User.username).join(User, Prediction.user_id == User.id).filter(Prediction.match_id == match_id).all()
    
    return [
        {
            "username": username,
            "predicted_home_goals": p.predicted_home_goals,
            "predicted_away_goals": p.predicted_away_goals
        }
        for p, username in predictions
    ]

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
    from app.models.models import User, ScoringRule, PhaseMultiplier
    
    # 1. Get active scoring rule
    rule = db.query(ScoringRule).filter(ScoringRule.is_active == True).first()
    if not rule:
        return []
    
    # 2. Get all predictions for finished matches, including the match's phase
    predictions = db.query(Prediction, Match).join(Match, Prediction.match_id == Match.id).filter(Match.status == "finished").all()
    
    # 3. Calculate breakdown per user
    user_stats = {} # {username: {exact: 0, winner: 0, home: 0, away: 0, total: 0}}
    
    users_map = {u.id: u.username for u in db.query(User).all()}
    
    for pred, match in predictions:
        username = users_map.get(pred.user_id)
        if not username: continue
        
        if username not in user_stats:
            user_stats[username] = {"exact": 0, "winner": 0, "home": 0, "away": 0, "total": 0}
        
        stats = user_stats[username]
        
        # Get the multiplier for this match's phase
        multiplier_obj = db.query(PhaseMultiplier).filter(PhaseMultiplier.id == match.phase_id).first()
        multiplier = multiplier_obj.multiplier if multiplier_obj else 1
        
        # Home Goals
        if pred.predicted_home_goals == match.home_goals:
            pts = rule.correct_home_goals_points * multiplier
            stats["home"] += pts
            stats["total"] += pts
            
        # Away Goals
        if pred.predicted_away_goals == match.away_goals:
            pts = rule.correct_away_goals_points * multiplier
            stats["away"] += pts
            stats["total"] += pts
            
        # Winner
        pred_winner = "home" if pred.predicted_home_goals > pred.predicted_away_goals else ("away" if pred.predicted_home_goals < pred.predicted_away_goals else "draw")
        actual_winner = "home" if match.home_goals > match.away_goals else ("away" if match.home_goals < match.away_goals else "draw")
        if pred_winner == actual_winner:
            pts = rule.correct_winner_points * multiplier
            stats["winner"] += pts
            stats["total"] += pts
            
        # Exact Score
        if pred.predicted_home_goals == match.home_goals and pred.predicted_away_goals == match.away_goals:
            pts = rule.correct_score_points * multiplier
            stats["exact"] += pts
            stats["total"] += pts
    
    # 4. Format for response and sort by total points
    leaderboard = []
    for username, stats in user_stats.items():
        leaderboard.append({
            "username": username,
            "total_points": stats["total"],
            "exact_score_pts": stats["exact"],
            "winner_pts": stats["winner"],
            "home_goals_pts": stats["home"],
            "away_goals_pts": stats["away"]
        })
    
    leaderboard.sort(key=lambda x: x["total_points"], reverse=True)
    return leaderboard
