from fastapi import FastAPI
from app.api.endpoints import auth, matches, predictions, rules, teams
from app.db.session import engine
from app.models.models import Base

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="World Cup Prediction API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
app.include_router(rules.router, prefix="/rules", tags=["Scoring Rules"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])

@app.get("/")
def read_root():
    return {"message": "Welcome to World Cup Prediction API"}
