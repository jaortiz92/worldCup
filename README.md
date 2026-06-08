# 🏆 World Cup 2026 Prediction Platform

A full-stack application designed for predicting World Cup 2026 match results. The platform features a competitive leaderboard with a dynamic, progressive scoring system to maintain user engagement throughout the tournament.

## 🚀 Features

### For Users
- **Match Predictions**: Predict scores for upcoming matches.
- **Real-time Leaderboard**: Track rankings based on prediction accuracy.
- **Detailed Breakdown**: View points earned for exact scores, winners, and individual team goals.
- **Responsive Design**: Fully optimized for both desktop and mobile devices.

### For Administrators
- **Match Management**: Create, edit (date and phase), and delete matches.
- **Dynamic Scoring Rules**: Configure base points for different types of hits.
- **Progressive Multipliers**: Manage scoring multipliers that increase as the tournament progresses (e.g., Final match points are worth more than Group Stage points).

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Logic**: Custom scoring engine with phase-based multipliers.

### Frontend
- **Framework**: Vue 3 (Composition API)
- **State Management**: Pinia
- **Styling**: Custom CSS with responsive breakpoints.
- **Build Tool**: Vite

## 📂 Project Structure

```text
├── backend/            # FastAPI Application
│   ├── app/
│   │   ├── api/        # Endpoints (auth, matches, predictions, rules, teams)
│   │   ├── models/     # SQLAlchemy Models
│   │   ├── schemas/    # Pydantic Schemas
│   │   ├── services/   # Business logic (scoring engine)
│   │   └── db/         # Database session and configuration
├── frontend/           # Vue.js Application
│   ├── src/
│   │   ├── api/        # API Client configuration
│   │   ├── components/ # Reusable UI components
│   │   ├── stores/     # Pinia stores for state management
│   │   ├── views/      # Page views (Home, Admin, Match Predictions)
│   │   └── utils/      # Helper functions (date formatting)
└── docs/               # Functional specifications and documentation
```

## ⚙️ Installation & Setup

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## 📈 Scoring Logic

The platform uses a **Base Score $\times$ Phase Multiplier** system:
- **Base Score**: Calculated from correct home goals, away goals, winner, and exact score.
- **Phase Multiplier**: Increases as the tournament advances (e.g., Group Stage $\times 1 \rightarrow$ Finals $\times 5$).
