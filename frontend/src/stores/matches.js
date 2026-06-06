import { defineStore } from 'pinia';
import apiClient from '../api/client';

export const useMatchesStore = defineStore('matches', {
  state: () => ({
    matches: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchMatches() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/matches/');
        this.matches = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to fetch matches';
      } finally {
        this.loading = false;
      }
    },
    async createMatch(matchData) {
      try {
        const response = await apiClient.post('/matches/', matchData);
        this.matches.push(response.data);
        return response.data;
      } catch (err) {
        throw err;
      }
    },
    async updateMatch(matchId, updateData) {
      try {
        const response = await apiClient.patch(`/matches/${matchId}`, updateData);
        const index = this.matches.findIndex(m => m.id === matchId);
        if (index !== -1) {
          this.matches[index] = response.data;
        }
        return response.data;
      } catch (err) {
        throw err;
      }
    },
  },
});
