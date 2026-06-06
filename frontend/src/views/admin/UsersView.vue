<script setup>
import { ref } from 'vue';
import apiClient from '../../api/client';

const newUser = ref({
  username: '',
  password: '',
});
const loading = ref(false);
const success = ref(false);
const error = ref(null);

const handleCreateUser = async () => {
  loading.value = true;
  success.value = false;
  error.value = null;
  try {
    await apiClient.post('/auth/users', newUser.value);
    success.value = true;
    newUser.value = { username: '', password: '' };
   } catch (err) {
     error.value = err.response?.data?.detail || 'Error al crear el usuario';
   } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div>
     <div class="mb-2">
       <h1>Gestionar Usuarios</h1>
     </div>
 
     <div class="card" style="max-width: 500px;">
       <h2>Crear Nuevo Usuario</h2>
       <form @submit.prevent="handleCreateUser">
         <div class="form-group">
           <label>Usuario</label>
           <input v-model="newUser.username" type="text" class="form-control" required />
         </div>
         <div class="form-group">
           <label>Contraseña</label>
           <input v-model="newUser.password" type="password" class="form-control" required />
         </div>
        <div v-if="error" class="error-message">{{ error }}</div>
         <div v-if="success" class="text-center" style="color: green; margin-bottom: 1rem; font-weight: bold;">
           ¡Usuario creado con éxito!
         </div>
         <button type="submit" class="btn btn-primary" :disabled="loading" style="width: 100%">
           {{ loading ? 'Creando...' : 'Crear Usuario' }}
         </button>
      </form>
    </div>
  </div>
</template>
