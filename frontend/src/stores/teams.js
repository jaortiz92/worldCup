import { defineStore } from 'pinia';
import apiClient from '../api/client';

export const useTeamsStore = defineStore('teams', {
  state: () => ({
    teams: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchTeams() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/teams/');
        this.teams = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to fetch teams';
      } finally {
        this.loading = false;
      }
    },
    async createTeam(teamData) {
      try {
        const response = await apiClient.post('/teams/', teamData);
        this.teams.push(response.data);
        return response.data;
      } catch (err) {
        throw err;
      }
    },
    async deleteTeam(teamId) {
      try {
        await apiClient.delete(`/teams/${teamId}`);
        this.teams = this.teams.filter(t => t.id !== teamId);
      } catch (err) {
        throw err;
      }
    },
  },
});
