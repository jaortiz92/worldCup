<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useMatchesStore } from '../stores/matches';
import apiClient from '../api/client';

const route = useRoute();
const authStore = useAuthStore();
const matchesStore = useMatchesStore();

const matchId = route.params.id;
const match = ref(null);
const predictions = ref([]);
const activeRule = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchAllData = async () => {
  loading.value = true;
  error.value = null;
  try {
    // 1. Fetch match details
    const matchResponse = await apiClient.get(`/matches/${matchId}`);
    match.value = matchResponse.data;

    // 2. Fetch predictions for this match
    const predResponse = await apiClient.get(`/predictions/match/${matchId}`);
    predictions.value = predResponse.data.sort((a, b) => a.username.localeCompare(b.username));

    // 3. Fetch active scoring rule
    const rulesResponse = await apiClient.get('/rules/');
    activeRule.value = rulesResponse.data.find(r => r.is_active);

  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar los datos del partido';
  } finally {
    loading.value = false;
  }
};

const calculatePoints = (prediction) => {
  if (!match.value || match.value.status !== 'finished' || !activeRule.value) return 0;

  let points = 0;
  const rule = activeRule.value;
  const actualHome = match.value.home_goals;
  const actualAway = match.value.away_goals;

  // Home Goals
  if (prediction.predicted_home_goals === actualHome) {
    points += rule.correct_home_goals_points;
  }
  // Away Goals
  if (prediction.predicted_away_goals === actualAway) {
    points += rule.correct_away_goals_points;
  }
  // Winner
  const predWinner = prediction.predicted_home_goals > prediction.predicted_away_goals ? 'home' : 
                     (prediction.predicted_home_goals < prediction.predicted_away_goals ? 'away' : 'draw');
  const actualWinner = actualHome > actualAway ? 'home' : 
                       (actualHome < actualAway ? 'away' : 'draw');
  if (predWinner === actualWinner) {
    points += rule.correct_winner_points;
  }
  // Exact Score
  if (prediction.predicted_home_goals === actualHome && prediction.predicted_away_goals === actualAway) {
    points += rule.correct_score_points;
  }

  return points;
};

const getRowClass = (prediction) => {
  if (!match.value || match.value.status !== 'finished') return '';

  const actualHome = match.value.home_goals;
  const actualAway = match.value.away_goals;
  
  if (prediction.predicted_home_goals === actualHome && prediction.predicted_away_goals === actualAway) {
    return 'row-exact';
  }

  const predWinner = prediction.predicted_home_goals > prediction.predicted_away_goals ? 'home' : 
                     (prediction.predicted_home_goals < prediction.predicted_away_goals ? 'away' : 'draw');
  const actualWinner = actualHome > actualAway ? 'home' : 
                       (actualHome < actualAway ? 'away' : 'draw');
  
  if (predWinner === actualWinner) {
    return 'row-winner';
  }
  
  return '';
};

onMounted(fetchAllData);
</script>

<template>
  <div class="predictions-view">
    <div class="header">
      <router-link to="/" class="back-btn">← Volver al Panel</router-link>
      <div class="match-info">
        <div class="teams-display">
          <div class="team">
            <img v-if="match?.home_team?.flag_url" :src="match.home_team.flag_url" class="flag" />
            <span class="name">{{ match?.home_team?.name || 'Cargando...' }}</span>
          </div>
          <div class="vs-score">
            <span v-if="match?.status === 'finished'" class="final-score">
              {{ match.home_goals }} - {{ match.away_goals }}
            </span>
            <span v-else class="vs-text">VS</span>
          </div>
          <div class="team">
            <img v-if="match?.away_team?.flag_url" :src="match.away_team.flag_url" class="flag" />
            <span class="name">{{ match?.away_team?.name || 'Cargando...' }}</span>
          </div>
        </div>
        <div class="match-details">
          <span class="date">{{ match?.match_date }}</span>
          <span :class="['status-badge', `status-${match?.status}`]">{{ match?.status }}</span>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">Cargando predicciones...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else class="predictions-container">
      <div class="predictions-card">
        <h3>Predicciones de los Participantes</h3>
        
        <table class="predictions-table">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>Predicción</th>
              <th v-if="match?.status === 'finished'">Puntos</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pred in predictions" :key="pred.username" 
                :class="[getRowClass(pred), { 'is-me': pred.username === authStore.user?.username }]">
              <td class="user-cell">
                <span v-if="pred.username === authStore.user?.username" class="me-icon">👤</span>
                {{ pred.username }}
              </td>
              <td class="score-cell">
                <span :class="['goal', { 'correct': match?.status === 'finished' && pred.predicted_home_goals === match?.home_goals, 'wrong': match?.status === 'finished' && pred.predicted_home_goals !== match?.home_goals }]">
                  {{ pred.predicted_home_goals }}
                </span>
                <span class="separator">-</span>
                <span :class="['goal', { 'correct': match?.status === 'finished' && pred.predicted_away_goals === match?.away_goals, 'wrong': match?.status === 'finished' && pred.predicted_away_goals !== match?.away_goals }]">
                  {{ pred.predicted_away_goals }}
                </span>
                <span v-if="getRowClass(pred) === 'row-exact'" class="winner-badge">🏆</span>
              </td>
              <td v-if="match?.status === 'finished'" class="points-cell">
                {{ calculatePoints(pred) }} pts
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.predictions-view {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.header {
  margin-bottom: 2rem;
}

.back-btn {
  text-decoration: none;
  color: var(--primary-color);
  font-weight: 500;
  display: inline-block;
  margin-bottom: 1.5rem;
}

.match-info {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow);
  text-align: center;
  border: 1px solid #eee;
}

.teams-display {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1rem;
}

.team {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  min-width: 150px;
}

.flag {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.name {
  font-weight: bold;
  font-size: 1.2rem;
}

.vs-score {
  font-size: 2rem;
  font-weight: 900;
  color: var(--primary-color);
}

.final-score {
  background: #eee;
  padding: 0 15px;
  border-radius: 8px;
}

.vs-text {
  color: gray;
  font-style: italic;
}

.match-details {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  color: gray;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: bold;
}
.status-pending { background: #fff3cd; color: #856404; }
.status-in_progress { background: #cce5ff; color: #004085; }
.status-finished { background: #d4edda; color: #155724; }

.predictions-container {
  margin-top: 2rem;
}

.predictions-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: var(--shadow);
  border: 1px solid #eee;
}

.predictions-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: var(--secondary-color);
  text-align: center;
}

.predictions-table {
  width: 100%;
  border-collapse: collapse;
}

.predictions-table th {
  text-align: left;
  padding: 12px;
  color: gray;
  font-weight: 500;
  border-bottom: 2px solid #eee;
}

.predictions-table td {
  padding: 12px;
  border-bottom: 1px solid #f8f9fa;
}

.user-cell {
  font-weight: 500;
}

.me-icon {
  margin-right: 6px;
}

.score-cell {
  text-align: center;
  font-weight: bold;
  font-size: 1.1rem;
}

.goal {
  padding: 2px 6px;
  border-radius: 4px;
}

.correct {
  color: #28a745;
}

.wrong {
  color: #dc3545;
}

.separator {
  margin: 0 8px;
  color: #ccc;
}

.winner-badge {
  margin-left: 10px;
  font-size: 1.2rem;
}

.points-cell {
  text-align: right;
  font-weight: bold;
  color: var(--primary-color);
}

/* Row styles */
.row-exact {
  background-color: #eaffea;
  border-left: 5px solid #28a745;
}

.row-winner {
  background-color: #fffdeb;
  border-left: 5px solid #ffd43b;
}

.is-me {
  outline: 2px solid var(--primary-color);
  background-color: #f0f5ff;
}

.loading-state, .error-message {
  text-align: center;
  padding: 2rem;
  color: gray;
}

.error-message {
  color: red;
}
</style>
