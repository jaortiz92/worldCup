from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # 'admin' or 'user'
    token_version = Column(Integer, default=0)

    predictions = relationship("Prediction", back_populates="user")


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    flag_url = Column(String, nullable=True)
    code_iso = Column(String, nullable=True)
    groups = Column(String, nullable=True)


class PhaseMultiplier(Base):
    __tablename__ = "phase_multipliers"
    id = Column(Integer, primary_key=True, index=True)
    phase_name = Column(String, unique=True, nullable=False)
    multiplier = Column(Integer, default=1)


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    home_goals = Column(Integer, default=0)
    away_goals = Column(Integer, default=0)
    match_date = Column(DateTime, nullable=False)  # UTC
    # 'pending', 'in_progress', 'finished'
    status = Column(String, default="pending")
    # 'Group Stage', 'Round of 32/16', 'Quarter-finals', 'Semi-finals', 'Finals'
    phase_id = Column(Integer, ForeignKey("phase_multipliers.id"), default=1)

    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    phase = relationship("PhaseMultiplier", foreign_keys=[phase_id])
    predictions = relationship("Prediction", back_populates="match")


class ScoringRule(Base):
    __tablename__ = "scoring_rules"
    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String, nullable=False)
    correct_score_points = Column(Integer, default=5)
    correct_winner_points = Column(Integer, default=2)
    correct_home_goals_points = Column(Integer, default=1)
    correct_away_goals_points = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    predicted_home_goals = Column(Integer, nullable=False)
    predicted_away_goals = Column(Integer, nullable=False)
    points_earned = Column(Integer, default=0)

    user = relationship("User", back_populates="predictions")
    match = relationship("Match", back_populates="predictions")
