from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timezone
from typing import List
from app.db.session import get_db
from app.models.models import Match
from app.schemas import schemas
from app.api.deps import get_admin_user
from app.services.scoring import calculate_match_points

router = APIRouter()


@router.get("/", response_model=List[schemas.MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return db.query(Match).order_by(Match.match_date.desc()).all()


@router.get("/{match_id}", response_model=schemas.MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


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

    # Validate date update restriction
    if "match_date" in match_in.dict(exclude_unset=True):
        if db_match.status not in ["pending", "in_progress"] and db_match.match_date.replace(
                tzinfo=timezone.utc) != match_in.match_date:
            raise HTTPException(
                status_code=400,
                detail="Match date can only be edited for pending or in-progress matches"
            )

    for var, value in match_in.dict(exclude_unset=True).items():
        setattr(db_match, var, value)

    db.commit()
    db.refresh(db_match)

    # Trigger scoring engine if status becomes 'finished'
    if db_match.status == "finished":
        calculate_match_points(db, match_id)

    return db_match


@router.delete("/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Check if predictions exist
    if db_match.predictions:
        raise HTTPException(
            status_code=400,
            detail="Match cannot be deleted because it already has predictions"
        )

    db.delete(db_match)
    db.commit()
    return {"detail": "Match deleted successfully"}
