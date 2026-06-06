<script setup>
import { onMounted } from 'vue';
import { useMatchesStore } from '../stores/matches';
import { usePredictionsStore } from '../stores/predictions';
import MatchesStatus from '../components/MatchesStatus.vue';

const matchesStore = useMatchesStore();
const predictionsStore = usePredictionsStore();

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
                 class="leaderboard-item" :class="{'top-3': index < 3, 'rank-1': index === 0}">
              <div class="rank">#{{ index + 1 }}</div>
              <div class="user-info">
                <span class="username">{{ entry.username }}</span>
              </div>
              <div class="points">
                <span class="points-value">{{ entry.total_points }}</span>
                <span class="points-label">pts</span>
              </div>
            </div>
          </div>
        </div>
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
.leaderboard-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 10px;
  background: #f8f9fa;
  transition: background 0.2s;
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
}
.leaderboard-item.top-3 {
  background: #fffdf0;
  border: 1px solid #ffeeba;
}
.leaderboard-item.rank-1 {
  background: #fff9db;
  border: 2px solid #ffd43b;
}
.rank {
  width: 30px;
  font-weight: bold;
  color: gray;
}
.user-info {
  flex: 1;
  font-weight: 500;
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

.loading-state {
  text-align: center;
  padding: 2rem;
  color: gray;
}
</style>


