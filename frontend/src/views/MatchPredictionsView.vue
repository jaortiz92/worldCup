<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useMatchesStore } from '../stores/matches';
import { formatToLocalTime } from '../utils/date';
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

  const multiplier = match.value.phase?.multiplier || 1;
  return points * multiplier;
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
          <span class="date">{{ formatToLocalTime(match?.match_date) }} <b>{{ match?.phase?.phase_name  }}</b></span>
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
                <td class="user-cell" data-label="Usuario">
                  <span v-if="pred.username === authStore.user?.username" class="me-icon">👤</span>
                  {{ pred.username }}
                </td>
                <td class="score-cell" data-label="Predicción">
                  <div class="score-wrapper">
                    <span :class="['goal', { 'correct': match?.status === 'finished' && pred.predicted_home_goals === match?.home_goals, 'wrong': match?.status === 'finished' && pred.predicted_home_goals !== match?.home_goals }]">
                      {{ pred.predicted_home_goals }}
                    </span>
                    <span class="separator">-</span>
                    <span :class="['goal', { 'correct': match?.status === 'finished' && pred.predicted_away_goals === match?.away_goals, 'wrong': match?.status === 'finished' && pred.predicted_away_goals !== match?.away_goals }]">
                      {{ pred.predicted_away_goals }}
                    </span>
                  </div>
                  <span v-if="getRowClass(pred) === 'row-exact'" class="winner-badge">🏆</span>
                </td>
                <td v-if="match?.status === 'finished'" class="points-cell" data-label="Puntos">
                  <span class="points-amount">{{ calculatePoints(pred) }}</span>
                  <span class="points-unit">pts</span>
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

@media (max-width: 768px) {
  .match-info {
    padding: 1rem;
  }
}

.teams-display {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1rem;
}

@media (max-width: 600px) {
  .teams-display {
    flex-direction: column;
    gap: 1rem;
  }
  .vs-score {
    font-size: 1.5rem;
    margin: 0.5rem 0;
  }
}

.team {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  min-width: 150px;
}

@media (max-width: 600px) {
  .team {
    min-width: 0;
    width: auto;
  }
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

@media (max-width: 768px) {
  .predictions-card {
    padding: 1rem;
  }
}

.predictions-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: var(--secondary-color);
  text-align: center;
}

.predictions-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px;
}

.predictions-table th {
  text-align: left;
  padding: 12px;
  color: #f8f8f8;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: none;
}

.predictions-table td {
  padding: 16px 12px;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.predictions-table tr td:first-child {
  border-left: 1px solid #f0f0f0;
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
}

.predictions-table tr td:last-child {
  border-right: 1px solid #f0f0f0;
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
}

.user-cell {
  font-weight: 600;
  color: #333;
  word-break: break-word;
  overflow-wrap: anywhere;
}

.me-icon {
  margin-right: 8px;
}

.score-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  font-weight: bold;
  font-size: 1.1rem;
}

.score-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.goal {
  padding: 4px 8px;
  border-radius: 6px;
  min-width: 24px;
  text-align: center;
  transition: all 0.2s;
}

.correct {
  color: #28a745;
  background: rgba(40, 167, 69, 0.1);
}

.wrong {
  color: #dc3545;
  background: rgba(220, 53, 69, 0.1);
}

.separator {
  color: #ccc;
  font-weight: normal;
}

.winner-badge {
  position: absolute;
  right: 10px;
  font-size: 1.2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.points-cell {
  text-align: right;
  font-weight: 700;
  color: var(--primary-color);
  white-space: nowrap;
}

.points-amount {
  font-size: 1.1rem;
}

.points-unit {
  font-size: 0.7rem;
  color: gray;
  margin-left: 4px;
  text-transform: uppercase;
}

/* Row styles */
.row-exact {
  background-color: #e6ffe6;
  transition: background 0.2s;
}

.row-winner {
  background-color: #f8f5c6;
  transition: background 0.2s;
}

.is-me {
  box-shadow: inset 4px 0 0 var(--primary-color);
}

.predictions-table tr:hover td {
  background-color: rgba(0,0,0,0.02);
}

@media (max-width: 768px) {
  .predictions-table thead {
    display: none;
  }

  .predictions-table, .predictions-table tbody, .predictions-table tr, .predictions-table td {
    display: block;
    width: 100%;
  }

  .predictions-table tr {
    margin-bottom: 1rem;
    border: 1px solid #eee;
    border-radius: 12px;
    padding: 8px;
    box-sizing: border-box;
  }

  .predictions-table td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: right;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #f9f9f9;
  }

  .predictions-table td:last-child {
    border-bottom: none;
  }
  
  .predictions-table td::before {
    content: attr(data-label);
    font-weight: 600;
    color: #888;
    text-align: left;
    font-size: 0.85rem;
    text-transform: uppercase;
  }
  
  .predictions-table tr td:first-child,
  .predictions-table tr td:last-child {
    border-left: none;
    border-right: none;
  }
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
