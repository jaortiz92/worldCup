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
       <h2>Iniciar sesión</h2>
       <p class="mb-2">Ingrese sus credenciales para acceder a la plataforma</p>
      
      <div v-if="authStore.error" class="error-message">
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleLogin">
         <div class="form-group">
           <label for="username">Usuario</label>
           <input 
             id="username" 
             v-model="username" 
             type="text" 
             class="form-control" 
             required 
             placeholder="Su usuario"
           />
         </div>
         <div class="form-group">
           <label for="password">Contraseña</label>
           <input 
             id="password" 
             v-model="password" 
             type="password" 
             class="form-control" 
             required 
             placeholder="Su contraseña"
           />
         </div>
         <button type="submit" class="btn btn-primary" :disabled="authStore.loading" style="width: 100%">
           {{ authStore.loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
         </button>
      </form>
    </div>
  </div>
</template>
