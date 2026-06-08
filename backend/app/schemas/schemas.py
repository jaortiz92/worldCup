from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

class PasswordChangeMe(BaseModel):
    current_password: str
    new_password: str

class PasswordChangeAdmin(BaseModel):
    new_password: str

class TeamBase(BaseModel):
    name: str
    flag_url: Optional[str] = None
    code_iso: Optional[str] = None
    groups: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamOut(TeamBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    match_date: datetime

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    status: Optional[str] = None

class MatchOut(MatchBase):
    id: int
    home_goals: int
    away_goals: int
    status: str
    home_team: Optional[TeamOut] = None
    away_team: Optional[TeamOut] = None
    class Config:
        from_attributes = True

class ScoringRuleBase(BaseModel):
    rule_name: str
    correct_score_points: int
    correct_winner_points: int
    correct_home_goals_points: int
    correct_away_goals_points: int
    is_active: bool = True

class ScoringRuleCreate(ScoringRuleBase):
    pass

class ScoringRuleOut(ScoringRuleBase):
    id: int
    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    match_id: int
    predicted_home_goals: int
    predicted_away_goals: int

class PredictionCreate(PredictionBase):
    pass

class PredictionUpdate(BaseModel):
    predicted_home_goals: Optional[int] = None
    predicted_away_goals: Optional[int] = None

class PredictionOut(PredictionBase):
    id: int
    user_id: int
    points_earned: int
    class Config:
        from_attributes = True

class MatchPredictionOut(BaseModel):
    username: str
    predicted_home_goals: int
    predicted_away_goals: int

class LeaderboardEntry(BaseModel):
    username: str
    total_points: int
    exact_score_pts: int = 0
    winner_pts: int = 0
    home_goals_pts: int = 0
    away_goals_pts: int = 0
