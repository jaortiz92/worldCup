<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<template>
  <div id="app">
    <nav class="navbar" v-if="authStore.isAuthenticated">
      <div class="container">
        <router-link to="/" style="color: white; text-decoration: none; font-size: 1.5rem; font-weight: bold;">
          🏆 WorldCup Quiniela
        </router-link>
        <ul class="nav-links">
          <li><router-link to="/">Dashboard</router-link></li>
          <li v-if="authStore.isAdmin">
            <router-link to="/admin/teams">Teams</router-link>
          </li>
          <li v-if="authStore.isAdmin">
            <router-link to="/admin/matches">Matches</router-link>
          </li>
          <li v-if="authStore.isAdmin">
            <router-link to="/admin/users">Users</router-link>
          </li>
          <li v-if="authStore.isAdmin">
            <router-link to="/admin/rules">Rules</router-link>
          </li>
          <li><a href="#" @click.prevent="handleLogout">Logout</a></li>
        </ul>
      </div>
    </nav>
    
    <main class="container mt-2">
      <router-view />
    </main>
  </div>
</template>
