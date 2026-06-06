<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');

const handleLogin = async () => {
  try {
    await authStore.login(username.value, password.value);
    router.push('/');
  } catch (err) {
    // Error is handled in store
  }
};
</script>

<template>
  <div class="login-container">
    <div class="card text-center">
      <h2>Login</h2>
      <p class="mb-2">Enter your credentials to access the platform</p>
      
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            id="username" 
            v-model="username" 
            type="text" 
            class="form-control" 
            required 
            placeholder="Your username"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            class="form-control" 
            required 
            placeholder="Your password"
          />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="authStore.loading" style="width: 100%">
          {{ authStore.loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>
