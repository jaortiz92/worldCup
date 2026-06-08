from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import User
from app.schemas import schemas
from app.core import security
from app.api.deps import get_admin_user, get_current_user

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "form-data"},
        )
    
    access_token = security.create_access_token(data={"sub": user.username, "token_version": user.token_version})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(User).all()

@router.post("/users", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    db_user = db.query(User).filter(User.username == user_in.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = security.get_password_hash(user_in.password)
    new_user = User(username=user_in.username, hashed_password=hashed_pw, role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.patch("/me/password")
def change_password_me(
    password_data: schemas.PasswordChangeMe, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    if not security.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password does not match",
        )
    
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long",
        )
    
    current_user.hashed_password = security.get_password_hash(password_data.new_password)
    current_user.token_version += 1
    db.commit()
    return {"detail": "Password successfully updated"}

@router.patch("/users/{user_id}/password")
def change_password_admin(
    user_id: int, 
    password_data: schemas.PasswordChangeAdmin, 
    db: Session = Depends(get_db), 
    admin=Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long",
        )
    
    user.hashed_password = security.get_password_hash(password_data.new_password)
    user.token_version += 1
    db.commit()
    return {"detail": "Password successfully updated"}
