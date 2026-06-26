<script setup>
import { ref, computed } from 'vue';
import { useMatchesStore } from '../stores/matches';
import { usePredictionsStore } from '../stores/predictions';
import { formatToLocalTime, isSameDayLocal } from '../utils/date';

const matchesStore = useMatchesStore();
const predictionsStore = usePredictionsStore();

const activeTab = ref('today');

const getPrediction = (matchId) => {
  return predictionsStore.myPredictions.find(p => p.match_id === matchId);
};

const getMatchPredictionStatus = (match) => {
  if (match.status !== 'finished') return '';
  const pred = getPrediction(match.id);
  if (!pred) return '';

  const actualHome = match.home_goals;
  const actualAway = match.away_goals;

  if (pred.predicted_home_goals === actualHome && pred.predicted_away_goals === actualAway) {
    return 'row-exact';
  }

  const predWinner = pred.predicted_home_goals > pred.predicted_away_goals ? 'home' : 
                     (pred.predicted_home_goals < pred.predicted_away_goals ? 'away' : 'draw');
  const actualWinner = actualHome > actualAway ? 'home' : 
                       (actualHome < actualAway ? 'away' : 'draw');

  if (predWinner === actualWinner) {
    return 'row-winner';
  }

  return '';
};

const filteredMatches = computed(() => {
  const matches = [...matchesStore.matches];
  const now = new Date();
  
  const filtered = matches.filter(match => {
    const matchDate = new Date(match.match_date.replace(' ', 'T') + (match.match_date.endsWith('Z') ? '' : 'Z'));
    const isToday = isSameDayLocal(match.match_date);
    const isPast = matchDate < now;
    const isFinished = match.status === 'finished';

    if (activeTab.value === 'today') {
      return isToday;
    } else if (activeTab.value === 'upcoming') {
      return !isToday && !isPast && !isFinished;
    } else if (activeTab.value === 'results') {
      return isFinished || isPast;
    }
    return true;
  });

  if (activeTab.value === 'today' || activeTab.value === 'upcoming') {
    return filtered.sort((a, b) => {
      return new Date(a.match_date) - new Date(b.match_date);
    });
  }

  return filtered;
});
</script>

<template>
  <div class="matches-column">
      <div class="section-title">
        <h2>Próximos Partidos</h2>
        <span class="badge-count">{{ filteredMatches.length }} partidos</span>
      </div>

      <div class="tabs-container">
        <button 
          @click="activeTab = 'today'" 
          :class="['tab-btn', { active: activeTab === 'today' }]"
        >
          📅 Hoy
        </button>
        <button 
          @click="activeTab = 'upcoming'" 
          :class="['tab-btn', { active: activeTab === 'upcoming' }]"
        >
          ⏳ Próximos
        </button>
        <button 
          @click="activeTab = 'results'" 
          :class="['tab-btn', { active: activeTab === 'results' }]"
        >
          ✅ Resultados
        </button>
      </div>
      
      <div v-if="matchesStore.loading" class="loading-state">Cargando partidos...</div>
     <div v-else-if="matchesStore.error" class="error-message">{{ matchesStore.error }}</div>
     <div v-else>
       <div v-if="filteredMatches.length === 0" class="empty-state">
         No hay partidos disponibles en esta categoría.
       </div>
        <div v-else class="matches-grid">
          <div v-for="match in filteredMatches" :key="match.id" 
               :class="['match-card', getMatchPredictionStatus(match)]">
             <span v-if="getMatchPredictionStatus(match) === 'row-exact'" class="winner-badge">🏆</span>
             <div class="card-header">
               <span class="match-date">{{ formatToLocalTime(match.match_date) }} <b>{{ match.phase.phase_name }}</b><span v-if="match.phase?.multiplier > 1" class="multiplier-badge">x{{ match.phase.multiplier }}</span></span>
              <span :class="['status-badge', `status-${match.status}`]">{{ match.status }}</span>
            </div>
            
            <div class="match-main">
              <div class="team home">
                <img v-if="match.home_team?.flag_url" :src="match.home_team.flag_url" class="team-flag" />
                <span class="team-name">{{ match.home_team?.name }}</span>
                 <div class="score-container">
                   <span v-if="match.status === 'finished'" class="final-score">{{ match.home_goals }}</span>
                   <span v-if="getPrediction(match.id)" 
                         :class="[
                           'predicted-score', 
                           { 'is-small': match.status === 'finished' },
                           { 'correct-prediction': match.status === 'finished' && getPrediction(match.id).predicted_home_goals === match.home_goals },
                           { 'wrong-prediction': match.status === 'finished' && getPrediction(match.id).predicted_home_goals !== match.home_goals }
                         ]">
                     {{ getPrediction(match.id).predicted_home_goals }}
                   </span>
                 </div>
              </div>
              
              <div class="match-vs">VS</div>
              
              <div class="team away">
                <img v-if="match.away_team?.flag_url" :src="match.away_team.flag_url" class="team-flag" />
                <span class="team-name">{{ match.away_team?.name }}</span>
                 <div class="score-container">
                   <span v-if="match.status === 'finished'" class="final-score">{{ match.away_goals }}</span>
                   <span v-if="getPrediction(match.id)" 
                         :class="[
                           'predicted-score', 
                           { 'is-small': match.status === 'finished' },
                           { 'correct-prediction': match.status === 'finished' && getPrediction(match.id).predicted_away_goals === match.away_goals },
                           { 'wrong-prediction': match.status === 'finished' && getPrediction(match.id).predicted_away_goals !== match.away_goals }
                         ]">
                     {{ getPrediction(match.id).predicted_away_goals }}
                   </span>
                 </div>
              </div>
            </div>
            
            <div class="card-footer">
                 <div class="footer-actions">
                   <router-link 
                     v-if="match.status === 'pending' || match.status === 'scheduled'" 
                     :to="`/predict/${match.id}`" 
                     class="btn-predict"
                   >
                     Predecir Marcador
                   </router-link>
                    <router-link 
                      :to="`/predictions-match/${match.id}`" 
                      class="btn-view-preds"
                    >
                      Ver Predicciones
                    </router-link>
                    <span v-if="match.status !== 'pending' && match.status !== 'scheduled'" class="locked-text">Cerrado 🔒</span>
                 </div>
            </div>
         </div>
       </div>
     </div>
  </div>
</template>

<style scoped>
.tabs-container {
  display: flex;
  gap: 10px;
  margin-bottom: 2rem;
  justify-content: center;
}

.tab-btn {
  padding: 8px 16px;
  border: none;
  background: #eee;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  color: gray;
}

.tab-btn.active {
  background: var(--primary-color);
  color: white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: gray;
  font-style: italic;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.section-title h2 {
  font-size: 1.5rem;
  color: var(--secondary-color);
}
.badge-count {
  background: var(--primary-color);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.match-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: var(--shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid #eee;
  position: relative;
}
.match-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.row-exact {
  background-color: #e6ffe6 !important;
}
.row-winner {
  background-color: #f8f5c6 !important;
}

.winner-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
  z-index: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  font-size: 0.85rem;
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

.match-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  text-align: center;
}
.team {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.team.away {
  flex-direction: column;
}
.team-name {
  font-weight: bold;
  font-size: 1.1rem;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.team-flag {
  width: 40px;
  height: 30px;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.score-container {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.final-score {
  color: var(--primary-color);
  background: #eee;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 1.5rem;
  font-weight: 900;
}
.predicted-score {
  color: var(--accent-color);
  font-style: italic;
  font-size: 1.2rem;
  font-weight: 700;
}
.predicted-score.is-small {
  font-size: 0.9rem;
  opacity: 0.8;
}

.correct-prediction {
  color: #28a745 !important;
  font-weight: 900 !important;
}

.wrong-prediction {
  color: #dc3545 !important;
  font-weight: 900 !important;
}

.match-vs {
  font-weight: 900;
  font-style: italic;
  color: var(--primary-color);
  font-size: 1.2rem;
  margin: 0 15px;
  opacity: 0.5;
}

.card-footer {
  margin-top: auto;
  width: 100%;
}
.footer-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  box-sizing: border-box;
}
.btn-predict {
  display: block;
  background: var(--accent-color);
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  width: 100%;
  text-align: center;
  transition: filter 0.2s;
  box-sizing: border-box;
}
.btn-view-preds {
  display: block;
  background: #f1f3f5;
  color: #495057;
  text-decoration: none;
  padding: 8px 20px;
  border-radius: 8px;
  font-weight: 500;
  width: 100%;
  text-align: center;
  transition: background 0.2s;
  font-size: 0.9rem;
  box-sizing: border-box;
}
.btn-view-preds:hover {
  background: #e9ecef;
}
.btn-predict:hover {
  filter: brightness(1.1);
}
.locked-text {
  display: block;
  text-align: center;
  color: gray;
  font-size: 0.9rem;
  font-weight: 500;
}

.multiplier-badge {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #000;
  font-weight: 900;
  font-size: 0.7rem;
  padding: 1px 6px;
  border-radius: 10px;
  margin-left: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  animation: pulse 2s infinite ease-in-out;
  display: inline-block;
  border: 1px solid #B8860B;
  vertical-align: middle;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: gray;
}
.error-message {
  text-align: center;
  padding: 2rem;
  color: red;
}
</style>
