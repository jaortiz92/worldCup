<template>
  <div class="profile-container">
    <div class="section-title">
      <h2>Ajustes de Seguridad</h2>
      <span class="badge-status">Cuenta</span>
    </div>

    <div class="profile-card">
      <h3>Cambiar Contraseña</h3>
      <p class="subtitle">Actualiza tu contraseña para mantener tu cuenta segura.</p>
      
      <form @submit.prevent="handlePasswordChange" class="password-form">
        <div class="form-group">
          <label for="currentPassword">Contraseña Actual</label>
          <input type="password" id="currentPassword" v-model="form.currentPassword" class="form-control" required />
        </div>
        <div class="form-group">
          <label for="newPassword">Nueva Contraseña</label>
          <input type="password" id="newPassword" v-model="form.newPassword" class="form-control" required />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirmar Nueva Contraseña</label>
          <input type="password" id="confirmPassword" v-model="form.confirmPassword" class="form-control" required />
        </div>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? 'Cambiando...' : 'Actualizar Contraseña' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const form = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
});

const error = ref('');
const loading = ref(false);

const handlePasswordChange = async () => {
  if (form.value.newPassword !== form.value.confirmPassword) {
    error.value = 'Las nuevas contraseñas no coinciden';
    return;
  }
  if (form.value.newPassword.length < 8) {
    error.value = 'La contraseña debe tener al menos 8 caracteres';
    return;
  }

  error.value = '';
  loading.value = true;

  try {
    await authStore.changePassword(form.value.currentPassword, form.value.newPassword);
    alert('Contraseña actualizada con éxito. Por favor, inicia sesión nuevamente.');
    router.push('/login');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cambiar la contraseña';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 0 1rem;
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

.badge-status {
  background: var(--primary-color);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
}

.profile-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: var(--shadow);
  border: 1px solid #eee;
  transition: transform 0.2s ease;
}

.profile-card h3 {
  margin-top: 0;
  color: #333;
  font-size: 1.25rem;
}

.subtitle {
  color: gray;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: left;
}

.form-group label {
  font-weight: 500;
  font-size: 0.9rem;
  color: #555;
}

.form-control {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0,0,0,0.05);
}

.error-message {
  color: #ff5252;
  font-size: 0.85rem;
  background: rgba(255, 82, 82, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  text-align: center;
}

.btn-submit {
  padding: 0.8rem;
  cursor: pointer;
  background: var(--accent-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  transition: filter 0.2s, transform 0.1s;
  margin-top: 1rem;
}

.btn-submit:hover {
  filter: brightness(1.1);
}

.btn-submit:active {
  transform: scale(0.98);
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
