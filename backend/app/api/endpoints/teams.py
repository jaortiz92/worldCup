from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Team
from app.schemas import schemas
from app.api.deps import get_admin_user

router = APIRouter()


@router.get("/", response_model=List[schemas.TeamOut])
def list_teams(db: Session = Depends(get_db)):
    return db.query(Team).order_by(Team.name).all()


@router.post("/", response_model=schemas.TeamOut)
def create_team(team_in: schemas.TeamCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_team = db.query(Team).filter(Team.name == team_in.name).first()
    if db_team:
        raise HTTPException(status_code=400, detail="Team already registered")

    new_team = Team(**team_in.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@router.get("/{team_id}", response_model=schemas.TeamOut)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return {"detail": "Team deleted successfully"}
