<script setup>
import { onMounted } from 'vue';
import { useMatchesStore } from '../stores/matches';
import { usePredictionsStore } from '../stores/predictions';

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
      <h1>🏆 Tournament Dashboard</h1>
      <p class="subtitle">Predict the scores and climb the leaderboard!</p>
    </div>

    <div class="dashboard-grid">
      <!-- Matches Section -->
      <div class="matches-column">
        <div class="section-title">
          <h2>Upcoming Matches</h2>
          <span class="badge-count">{{ matchesStore.matches.length }} matches</span>
        </div>
        
        <div v-if="matchesStore.loading" class="loading-state">Loading matches...</div>
        <div v-else-if="matchesStore.error" class="error-message">{{ matchesStore.error }}</div>
        <div v-else class="matches-grid">
          <div v-for="match in matchesStore.matches" :key="match.id" class="match-card">
            <div class="card-header">
              <span class="match-date">{{ new Date(match.match_date).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' }) }}</span>
              <span :class="['status-badge', `status-${match.status}`]">{{ match.status }}</span>
            </div>
            
            <div class="match-main">
              <div class="team home">
                <img v-if="match.home_team?.flag_url" :src="match.home_team.flag_url" class="team-flag" />
                <span class="team-name">{{ match.home_team?.name }}</span>
                <div class="score-container">
                  <span v-if="match.status === 'finished'" class="final-score">{{ match.home_goals }}</span>
                  <span v-else-if="predictionsStore.myPredictions.find(p => p.match_id === match.id)" class="predicted-score">
                    {{ predictionsStore.myPredictions.find(p => p.match_id === match.id).predicted_home_goals }}
                  </span>
                </div>
              </div>
              
              <div class="match-vs">VS</div>
              
              <div class="team away">
                <span class="team-name">{{ match.away_team?.name }}</span>
                <img v-if="match.away_team?.flag_url" :src="match.away_team.flag_url" class="team-flag" />
                <div class="score-container">
                  <span v-if="match.status === 'finished'" class="final-score">{{ match.away_goals }}</span>
                  <span v-else-if="predictionsStore.myPredictions.find(p => p.match_id === match.id)" class="predicted-score">
                    {{ predictionsStore.myPredictions.find(p => p.match_id === match.id).predicted_away_goals }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="card-footer">
              <router-link 
                v-if="match.status === 'pending' || match.status === 'scheduled'" 
                :to="`/predict/${match.id}`" 
                class="btn-predict"
              >
                Predict Score
              </router-link>
              <span v-else class="locked-text">Locked 🔒</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Leaderboard Section -->
      <div class="leaderboard-column">
        <div class="section-title">
          <h2>Leaderboard</h2>
          <span class="trophy-icon">🥇</span>
        </div>
        
        <div v-if="predictionsStore.loading" class="loading-state">Loading...</div>
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
.subtitle {
  color: gray;
  font-size: 1.1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
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
}
.match-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
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
  flex-direction: row-reverse;
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
  font-size: 1.5rem;
  font-weight: 900;
}
.final-score {
  color: var(--primary-color);
  background: #eee;
  padding: 2px 10px;
  border-radius: 4px;
}
.predicted-score {
  color: var(--accent-color);
  font-style: italic;
  font-size: 1.2rem;
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
  display: flex;
  justify-content: center;
}
.btn-predict {
  background: var(--accent-color);
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  width: 100%;
  text-align: center;
  transition: filter 0.2s;
}
.btn-predict:hover {
  filter: brightness(1.1);
}
.locked-text {
  color: gray;
  font-size: 0.9rem;
  font-weight: 500;
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

