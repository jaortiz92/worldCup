<script setup>
import { ref, onMounted, computed } from 'vue';
import apiClient from '../api/client';

const rules = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchActiveRule = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await apiClient.get('/rules/');
    rules.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar las reglas';
  } finally {
    loading.value = false;
  }
};

const activeRule = computed(() => {
  return rules.value.find(rule => rule.is_active);
});

onMounted(fetchActiveRule);
</script>

<template>
  <div class="rules-container">
    <div class="section-title">
      <h2>Reglas de Puntuación</h2>
      <span class="info-icon">ℹ️</span>
    </div>

    <div v-if="loading" class="loading-state">Cargando reglas...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else-if="!activeRule" class="empty-state">
      No hay reglas activas configuradas.
    </div>
    <div v-else class="rules-card">
      <div class="rules-list">
        <div class="rule-item">
          <span class="rule-icon">🎯</span>
          <div class="rule-details">
            <span class="rule-label">Marcador Exacto</span>
            <span class="rule-points">{{ activeRule.correct_score_points }} pts</span>
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">🏆</span>
          <div class="rule-details">
            <span class="rule-label">Ganador Correcto o Empate</span>
            <span class="rule-points">{{ activeRule.correct_winner_points }} pts</span>
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">🏠</span>
          <div class="rule-details">
            <span class="rule-label">Goles Local Correctos</span>
            <span class="rule-points">{{ activeRule.correct_home_goals_points }} pts</span>
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">🚩</span>
          <div class="rule-details">
            <span class="rule-label">Goles Visitante Correctos</span>
            <span class="rule-points">{{ activeRule.correct_away_goals_points }} pts</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rules-container {
  margin-top: 2rem;
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
  margin: 0;
}

.info-icon {
  font-size: 1.2rem;
}

.rules-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: var(--shadow);
  border: 1px solid #eee;
}

.rules-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 10px;
  border-radius: 10px;
  background: #f8f9fa;
  transition: background 0.2s;
}

.rule-item:hover {
  background: #f1f3f5;
}

.rule-icon {
  font-size: 1.5rem;
  width: 30px;
  text-align: center;
}

.rule-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.rule-label {
  font-weight: 500;
  color: #555;
  font-size: 0.95rem;
}

.rule-points {
  font-weight: bold;
  color: var(--primary-color);
  background: #eef2ff;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 0.9rem;
}

.loading-state, .error-message, .empty-state {
  text-align: center;
  padding: 2rem;
  color: gray;
}

.error-message {
  color: red;
}
</style>
