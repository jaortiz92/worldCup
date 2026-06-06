import { defineStore } from 'pinia';
import apiClient from '../api/client';

export const usePredictionsStore = defineStore('predictions', {
  state: () => ({
    leaderboard: [],
    myPredictions: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchMyPredictions() {
      try {
        const response = await apiClient.get('/predictions/me');
        this.myPredictions = response.data;
      } catch (err) {
        console.error('Failed to fetch predictions:', err);
      }
    },
    async fetchLeaderboard() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/predictions/leaderboard');
        this.leaderboard = response.data;
       } catch (err) {
         this.error = err.response?.data?.detail || 'Error al cargar la tabla de posiciones';
       } finally {
        this.loading = false;
      }
    },
    async createPrediction(predictionData) {
      try {
        const response = await apiClient.post('/predictions/', predictionData);
        return response.data;
      } catch (err) {
        throw err;
      }
    },
    async updatePrediction(matchId, predictionData) {
      try {
        const response = await apiClient.patch(`/predictions/${matchId}`, predictionData);
        return response.data;
      } catch (err) {
        throw err;
      }
    },
  },
});
