<script setup>
import { onMounted, ref } from 'vue';
import { useMatchesStore } from '../stores/matches';
import { usePredictionsStore } from '../stores/predictions';
import { useAuthStore } from '../stores/auth';
import MatchesStatus from '../components/MatchesStatus.vue';
import ScoringRules from '../components/ScoringRules.vue';

const matchesStore = useMatchesStore();
const predictionsStore = usePredictionsStore();
const authStore = useAuthStore();
const expandedUser = ref(null);

const toggleUser = (username) => {
  if (expandedUser.value === username) {
    expandedUser.value = null;
  } else {
    expandedUser.value = username;
  }
};

onMounted(async () => {
  await Promise.all([
    matchesStore.fetchMatches(),
    predictionsStore.fetchLeaderboard(),
    predictionsStore.fetchMyPredictions()
  ]);
});
</script>

<template>
  <div>
    <div class="header-section mb-2">
       <h1>🏆 Panel del Torneo</h1>
       <p class="subtitle">¡Prediga los marcadores y suba en la tabla de posiciones!</p>
    </div>

    <div class="dashboard-grid">
      <!-- Matches Section -->
      <MatchesStatus />

      <!-- Leaderboard Section -->
      <div class="leaderboard-column">
         <div class="section-title">
           <h2>Tabla de Posiciones</h2>
           <span class="trophy-icon">🥇</span>
         </div>
         
         <div v-if="predictionsStore.loading" class="loading-state">Cargando...</div>
        <div v-else-if="predictionsStore.error" class="error-message">{{ predictionsStore.error }}</div>
        <div v-else class="leaderboard-card">
          <div class="leaderboard-list">
            <div v-for="(entry, index) in predictionsStore.leaderboard" :key="entry.username" 
                 class="leaderboard-item-container">
              <div class="leaderboard-item" 
                   :class="{
                     'rank-1': index === 0, 
                     'rank-2': index === 1, 
                     'rank-3': index === 2, 
                     'is-me': entry.username === authStore.user?.username
                   }"
                   @click="toggleUser(entry.username)"
                   style="cursor: pointer">
                <div class="rank">
                  <span v-if="index === 0">🥇</span>
                  <span v-else-if="index === 1">🥈</span>
                  <span v-else-if="index === 2">🥉</span>
                  <span v-else>#{{ index + 1 }}</span>
                </div>
                <div class="user-info">
                  <span class="username">
                    <span v-if="entry.username === authStore.user?.username" class="me-icon">👤</span>
                    {{ entry.username }}
                  </span>
                </div>
                <div class="points">
                  <span class="points-value">{{ entry.total_points }}</span>
                  <span class="points-label">pts</span>
                </div>
              </div>

              <div v-if="expandedUser === entry.username || entry.username === authStore.user?.username" 
                   class="breakdown-container">
                <div class="breakdown-grid">
                  <div class="breakdown-item">
                    <span class="b-icon">🎯</span>
                    <span class="b-val">{{ entry.exact_score_pts }}</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="b-icon">🏆</span>
                    <span class="b-val">{{ entry.winner_pts }}</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="b-icon">🏠</span>
                    <span class="b-val">{{ entry.home_goals_pts }}</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="b-icon">🚩</span>
                    <span class="b-val">{{ entry.away_goals_pts }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <ScoringRules />
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-section {
  text-align: center;
  margin-bottom: 3rem;
}
.header-section h1 {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .header-section h1 {
    font-size: 1.8rem;
  }
  .header-section {
    margin-bottom: 2rem;
  }
}
.subtitle {
  color: gray;
  font-size: 1.1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
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

.leaderboard-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: var(--shadow);
}
.leaderboard-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.leaderboard-item-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 10px;
  background: #f8f9fa;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

@media (max-width: 480px) {
  .leaderboard-item {
    padding: 15px 12px;
  }
  .username {
    font-size: 0.9rem;
  }
}
.leaderboard-item:hover {
  background: #f1f3f5;
  transform: translateX(5px);
}

.leaderboard-item.rank-1 {
  background: linear-gradient(to right, #fff9db, #fff);
  border-color: #ffd43b;
  box-shadow: 0 4px 10px rgba(255, 212, 59, 0.2);
}
.leaderboard-item.rank-2 {
  background: linear-gradient(to right, #f1f3f5, #fff);
  border-color: #ced4da;
}
.leaderboard-item.rank-3 {
  background: linear-gradient(to right, #fff5f0, #fff);
  border-color: #e67e22;
}

.leaderboard-item.is-me {
  border-left: 4px solid var(--primary-color);
  background: #eef2ff;
}

.rank {
  width: 35px;
  font-weight: bold;
  color: gray;
  display: flex;
  justify-content: center;
}
.user-info {
  flex: 1;
  font-weight: 500;
}
.username {
  display: flex;
  align-items: center;
  gap: 6px;
}
.is-me .username {
  color: var(--primary-color);
  font-weight: 800;
}
.me-icon {
  font-size: 0.9rem;
}
.points {
  display: flex;
  align-items: baseline;
  gap: 4px;
}
.points-value {
  font-weight: bold;
  font-size: 1.2rem;
  color: var(--primary-color);
}
.points-label {
  font-size: 0.7rem;
  color: gray;
  text-transform: uppercase;
}

.breakdown-container {
  padding: 8px 12px 8px 45px;
  background: rgba(0,0,0,0.02);
  border-radius: 0 0 10px 10px;
  font-size: 0.8rem;
  animation: slideDown 0.2s ease-out;
}

.breakdown-grid {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 10px;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #666;
}

.b-icon {
  font-size: 1rem;
}

.b-val {
  font-weight: 600;
  color: #333;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: gray;
}
</style>




