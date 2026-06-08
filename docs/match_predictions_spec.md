# Feature Specification: Match Predictions View

## 1. User Story
As a user, I want to see the predictions made by all participants for a specific match so that I can compare my prediction with others and see who guessed the result correctly once the match is finished.

## 2. Technical Specification

### 2.1 API Endpoints

#### `GET /predictions/match/{match_id}`
- **Description**: Retrieves all predictions for a specific match along with the usernames of the participants.
- **Authentication**: Required (JWT).
- **Response**:
  ```json
  [
    {
      "username": "string",
      "predicted_home_goals": "integer",
      "predicted_away_goals": "integer"
    },
    ...
  ]
  ```

#### `GET /rules/`
- **Description**: Retrieves the active scoring rules to calculate points on the frontend.
- **Authentication**: Required (JWT).

### 2.2 Frontend Implementation

#### Route
- **Path**: `/predictions-match/:id`
- **Component**: `MatchPredictionsView.vue`
- **Meta**: `requiresAuth: true`

#### Integration in `MatchesStatus.vue`
- Add a "Ver Predicciones" button in the `card-footer` of each match card.
- This button should link to `/predictions-match/${match.id}`.

#### `MatchPredictionsView.vue` Logic
1. **Data Fetching**:
    - Fetch match details (teams, date, final score if finished).
    - Fetch all predictions for the match via `/predictions/match/{match_id}`.
    - Fetch active scoring rules via `/rules/`.
2. **Calculations (for Finished Matches)**:
    - Compare each user's prediction against the final match score.
    - Calculate points earned for that match based on the fetched scoring rules (Exact Score, Winner, Home Goals, Away Goals).
3. **Visual Rendering**:
    - **Header**: Display the two teams and the final result (if `status === 'finished'`).
    - **User List**:
        - Order participants alphabetically by `username`.
        - **Prediction Numbers**:
            - **Green**: If the predicted goal count matches the actual goal count.
            - **Red**: If the predicted goal count differs from the actual goal count.
        - **Row Background**:
            - **Green + 🏆 Icon**: If the user guessed the exact score.
            - **Yellow**: If the user guessed the winner (Home/Away/Draw) but not the exact score.
            - **Neutral**: Otherwise.
        - **Points Column**: Display the total points earned by the user in this specific match.
        - **User Highlight**: The currently logged-in user must be highlighted with a distinct style and a 👤 icon.

## 3. Assumptions
1. The list of predictions is sorted alphabetically by username.
2. The view is read-only; users cannot edit predictions here.
3. Access requires a valid JWT token.
4. Points calculation for the match is performed on the frontend using the active rules fetched from the API.
