<script setup>
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import DigitalClock from './DigitalClock.vue';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<template>
  <nav class="navbar" v-if="authStore.isAuthenticated">
    <div class="nav-container">
      <div class="nav-left">
        <router-link to="/" class="nav-logo">
          <span class="trophy">🏆</span> Polla Del Mundial
        </router-link>
      </div>

      <div class="nav-center">
        <ul class="nav-links">
          <li><router-link to="/" class="nav-link">Panel</router-link></li>
          <template v-if="authStore.isAdmin">
            <li><router-link to="/admin/matches" class="nav-link">Partidos</router-link></li>
            <li><router-link to="/admin/users" class="nav-link">Usuarios</router-link></li>
            <li><router-link to="/admin/rules" class="nav-link">Reglas</router-link></li>
            <li><router-link to="/admin/teams" class="nav-link">Equipos</router-link></li>
          </template>
        </ul>
      </div>

      <div class="nav-right">
        <DigitalClock />
        <button @click="handleLogout" class="logout-btn">
          Cerrar Sesión
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.75rem 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  flex: 1;
}

.nav-logo {
  color: rgb(12, 6, 6);
  text-decoration: none;
  font-size: 1.4rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: opacity 0.2s;
}

.nav-logo:hover {
  opacity: 0.8;
}

.trophy {
  font-size: 1.6rem;
}

.nav-center {
  flex: 2;
  display: flex;
  justify-content: center;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: rgba(2, 1, 1, 0.8);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: rgb(91, 88, 245);
  background: rgba(255, 255, 255, 0.1);
}

.router-link-active {
  color: rgb(46, 62, 243);
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.nav-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1.5rem;
}

.logout-btn {
  background: rgba(255, 82, 82, 0.2);
  color: #ff5252;
  border: 1px solid rgba(255, 82, 82, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.logout-btn:hover {
  background: #ff5252;
  color: white;
  box-shadow: 0 0 15px rgba(255, 82, 82, 0.4);
}

@media (max-width: 768px) {
  .nav-center {
    display: none;
  }
  .nav-container {
    padding: 0 1rem;
  }
}
</style>
