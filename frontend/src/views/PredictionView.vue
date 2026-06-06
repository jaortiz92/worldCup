<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMatchesStore } from '../stores/matches';
import { usePredictionsStore } from '../stores/predictions';

const route = useRoute();
const router = useRouter();
const matchesStore = useMatchesStore();
const predictionsStore = usePredictionsStore();

const matchId = parseInt(route.params.id);
const homeGoals = ref(0);
const awayGoals = ref(0);
const loading = ref(false);
const error = ref(null);
const success = ref(false);

const match = computed(() => matchesStore.matches.find(m => m.id === matchId));

const isLocked = computed(() => {
  if (!match.value || !match.value.match_date) return true;
  
  const dateStr = match.value.match_date;
  const utcDateStr = dateStr.endsWith('Z') ? dateStr : `${dateStr}Z`;
  const matchDate = new Date(utcDateStr);
  const now = new Date();
  
  if (isNaN(matchDate.getTime())) return true;
  return now.getTime() >= matchDate.getTime();
});

onMounted(async () => {
  await matchesStore.fetchMatches();
});

const submitPrediction = async () => {
  loading.value = true;
  error.value = null;
  success.value = false;
  try {
    const predictionData = {
      match_id: matchId,
      predicted_home_goals: homeGoals.value,
      predicted_away_goals: awayGoals.value,
    };
    
    try {
      await predictionsStore.createPrediction(predictionData);
    } catch (e) {
      if (e.response?.status === 400 && e.response?.data?.detail?.includes('already exists')) {
        await predictionsStore.updatePrediction(matchId, predictionData);
      } else {
        throw e;
      }
    }
    
    success.value = true;
    setTimeout(() => router.push('/'), 2000);
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to submit prediction';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div>
    <div class="flex align-center mb-2">
      <router-link to="/" class="back-link">
        ← Back to Dashboard
      </router-link>
    </div>

    <div class="prediction-container">
      <div class="prediction-card">
        <h2 class="text-center">Place Your Prediction</h2>
        
        <div v-if="!match" class="loading-state text-center">Loading match details...</div>
        <div v-else>
          <div class="scoreboard">
            <!-- Home Team -->
            <div class="team-section home">
              <div class="team-info">
                <img v-if="match.home_team?.flag_url" :src="match.home_team.flag_url" class="big-flag" />
                <span class="team-name">{{ match.home_team?.name }}</span>
              </div>
              <div class="score-input-container">
                <input 
                  v-if="!isLocked" 
                  v-model.number="homeGoals" 
                  type="number" 
                  min="0" 
                  class="score-input" 
                  required 
                />
                <span v-else class="locked-score">{{ match.home_goals ?? 0 }}</span>
              </div>
            </div>

            <div class="vs-divider">VS</div>

            <!-- Away Team -->
            <div class="team-section away">
              <div class="team-info">
                <span class="team-name">{{ match.away_team?.name }}</span>
                <img v-if="match.away_team?.flag_url" :src="match.away_team.flag_url" class="big-flag" />
              </div>
              <div class="score-input-container">
                <input 
                  v-if="!isLocked" 
                  v-model.number="awayGoals" 
                  type="number" 
                  min="0" 
                  class="score-input" 
                  required 
                />
                <span v-else class="locked-score">{{ match.away_goals ?? 0 }}</span>
              </div>
            </div>
          </div>

          <div class="match-meta text-center">
            <span class="date-label">Match Date: {{ new Date(match.match_date).toLocaleString() }}</span>
          </div>

          <div v-if="isLocked" class="lock-overlay">
            <div class="lock-content">
              <span class="lock-icon">🔒</span>
              <p>Predictions are locked because the match has already started or finished.</p>
            </div>
          </div>

          <form @submit.prevent="submitPrediction" v-if="!isLocked">
            <div v-if="error" class="error-message">{{ error }}</div>
            <div v-if="success" class="success-message">
              🎉 Prediction saved successfully! Redirecting...
            </div>

            <button type="submit" class="btn-submit" :disabled="loading">
              {{ loading ? 'Saving...' : 'Submit Prediction' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.back-link {
  text-decoration: none; 
  color: var(--primary-color); 
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 5px;
}

.prediction-container {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.prediction-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: var(--shadow);
  width: 100%;
  max-width: 800px;
  position: relative;
  overflow: hidden;
}

.scoreboard {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  margin: 3rem 0;
  background: #1a1a1a;
  padding: 40px;
  border-radius: 20px;
  color: white;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
}

.team-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
.team-section.away {
  text-align: right;
}
.team-info {
  display: flex;
  align-items: center;
  gap: 15px;
}
.team-section.away .team-info {
  flex-direction: row-reverse;
}
.team-name {
  font-size: 1.5rem;
  font-weight: bold;
  text-transform: uppercase;
}
.big-flag {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid rgba(255,255,255,0.2);
}

.score-input-container {
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.score-input {
  width: 80px;
  height: 80px;
  background: #333;
  border: 3px solid var(--accent-color);
  color: white;
  font-size: 2.5rem;
  font-weight: bold;
  text-align: center;
  border-radius: 12px;
}
.locked-score {
  font-size: 3rem;
  font-weight: bold;
  color: #666;
}

.vs-divider {
  font-size: 2rem;
  font-weight: 900;
  color: var(--accent-color);
  font-style: italic;
}

.match-meta {
  margin-bottom: 2rem;
}
.date-label {
  font-size: 1rem;
  color: gray;
  background: #eee;
  padding: 5px 15px;
  border-radius: 20px;
}

.lock-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}
.lock-content {
  text-align: center;
  padding: 20px;
}
.lock-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}

.btn-submit {
  background: var(--accent-color);
  color: white;
  border: none;
  padding: 15px 40px;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 12px;
  cursor: pointer;
  width: 100%;
  transition: transform 0.2s;
}
.btn-submit:hover {
  transform: scale(1.02);
}
.success-message {
  text-align: center;
  color: green;
  font-weight: bold;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
.loading-state {
  text-align: center;
  padding: 3rem;
  color: gray;
}
</style>

