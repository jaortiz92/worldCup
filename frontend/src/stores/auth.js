import { defineStore } from 'pinia';
import apiClient from '../api/client';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
  },
  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;
      try {
        // FastAPI OAuth2 requires application/x-www-form-urlencoded
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);

        const response = await apiClient.post('/auth/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        const { access_token } = response.data;

        this.token = access_token;
        localStorage.setItem('token', access_token);

        // Fetch user profile to get role
        await this.fetchProfile();
       } catch (err) {
         this.error = err.response?.data?.detail || 'Error al iniciar sesión';
         throw err;
       } finally {
        this.loading = false;
      }
    },
    async fetchProfile() {
      try {
        const response = await apiClient.get('/auth/me');
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
      } catch (err) {
        this.logout();
        throw err;
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    },
    async changePassword(currentPassword, newPassword) {
      try {
        await apiClient.patch('/auth/me/password', {
          current_password: currentPassword,
          new_password: newPassword,
        });
        this.logout();
        return true;
      } catch (err) {
        throw err;
      }
    },
    async changeUserPassword(userId, newPassword) {
      try {
        await apiClient.patch(`/auth/users/${userId}/password`, {
          new_password: newPassword,
        });
        return true;
      } catch (err) {
        throw err;
      }
    },
  },
});
