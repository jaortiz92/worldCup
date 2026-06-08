from sqlalchemy.orm import Session
from app.models.models import Match, Prediction, ScoringRule, PhaseMultiplier
from sqlalchemy import func


def calculate_match_points(db: Session, match_id: int):
    # 1. Fetch the match and the currently active scoring rules
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match or match.status != "finished":
        return

    rule = db.query(ScoringRule).filter(ScoringRule.is_active == True).first()
    if not rule:
        return  # Or use default points

    # Fetch the multiplier for the match's phase
    multiplier = match.phase.multiplier if match.phase else 1

    # 2. Fetch all predictions for this match
    predictions = db.query(Prediction).filter(
        Prediction.match_id == match_id).all()

    for pred in predictions:
        points = 0

        # 1. Correct Home Goals
        if pred.predicted_home_goals == match.home_goals:
            points += rule.correct_home_goals_points

        # 2. Correct Away Goals
        if pred.predicted_away_goals == match.away_goals:
            points += rule.correct_away_goals_points

        # 3. Correct Winner
        pred_winner = "home" if pred.predicted_home_goals > pred.predicted_away_goals else (
            "away" if pred.predicted_home_goals < pred.predicted_away_goals else "draw")
        actual_winner = "home" if match.home_goals > match.away_goals else (
            "away" if match.home_goals < match.away_goals else "draw")
        if pred_winner == actual_winner:
            points += rule.correct_winner_points

        # 4. Exact Score Bonus
        if pred.predicted_home_goals == match.home_goals and pred.predicted_away_goals == match.away_goals:
            points += rule.correct_score_points

        # Apply the progressive multiplier
        pred.points_earned = points * multiplier
        print(pred.points_earned)

    db.commit()
