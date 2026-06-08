<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../../api/client';
import { useAuthStore } from '../../stores/auth';

const authStore = useAuthStore();

const newUser = ref({
  username: '',
  password: '',
});
const users = ref([]);
const loading = ref(false);
const success = ref(false);
const error = ref(null);

const passwordChangeForm = ref({
  userId: null,
  newPassword: '',
});
const isPasswordModalOpen = ref(false);
const passwordLoading = ref(false);
const passwordError = ref(null);

const fetchUsers = async () => {
  try {
    const response = await apiClient.get('/auth/users');
    users.value = response.data;
  } catch (err) {
    console.error('Error fetching users:', err);
  }
};

const handleCreateUser = async () => {
  loading.value = true;
  success.value = false;
  error.value = null;
  try {
    await apiClient.post('/auth/users', newUser.value);
    success.value = true;
    newUser.value = { username: '', password: '' };
    await fetchUsers();
   } catch (err) {
     error.value = err.response?.data?.detail || 'Error al crear el usuario';
   } finally {
    loading.value = false;
  }
};

const openPasswordModal = (user) => {
  passwordChangeForm.value = { userId: user.id, newPassword: '' };
  passwordError.value = null;
  isPasswordModalOpen.value = true;
};

const handlePasswordChange = async () => {
  if (passwordChangeForm.value.newPassword.length < 8) {
    passwordError.value = 'La contraseña debe tener al menos 8 caracteres';
    return;
  }

  passwordLoading.value = true;
  passwordError.value = null;
  try {
    await authStore.changeUserPassword(passwordChangeForm.value.userId, passwordChangeForm.value.newPassword);
    alert('Contraseña actualizada con éxito');
    isPasswordModalOpen.value = false;
    passwordChangeForm.value = { userId: null, newPassword: '' };
  } catch (err) {
    passwordError.value = err.response?.data?.detail || 'Error al cambiar la contraseña';
  } finally {
    passwordLoading.value = false;
  }
};

onMounted(fetchUsers);
</script>

<template>
  <div>
     <div class="mb-2">
       <h1>Gestionar Usuarios</h1>
     </div>

     <div class="card" style="max-width: 500px; margin-bottom: 2rem;">
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

     <div class="card">
       <h2>Lista de Usuarios</h2>
       <table class="table">
         <thead>
           <tr>
             <th>ID</th>
             <th>Username</th>
             <th>Role</th>
             <th>Acciones</th>
           </tr>
         </thead>
         <tbody>
           <tr v-for="user in users" :key="user.id">
             <td>{{ user.id }}</td>
             <td>{{ user.username }}</td>
             <td>{{ user.role }}</td>
             <td>
               <button @click="openPasswordModal(user)" class="btn btn-secondary btn-sm">
                 Cambiar Clave
               </button>
             </td>
           </tr>
         </tbody>
       </table>
     </div>

     <!-- Password Change Modal -->
     <div v-if="isPasswordModalOpen" class="modal-overlay">
       <div class="modal">
         <h3>Cambiar Contraseña de Usuario</h3>
         <p>Usuario ID: {{ passwordChangeForm.userId }}</p>
         <div class="form-group">
           <label>Nueva Contraseña</label>
           <input v-model="passwordChangeForm.newPassword" type="password" class="form-control" required />
         </div>
         <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
         <div class="modal-actions">
           <button @click="isPasswordModalOpen = false" class="btn btn-secondary">Cancelar</button>
           <button @click="handlePasswordChange" class="btn btn-primary" :disabled="passwordLoading">
             {{ passwordLoading ? 'Cambiando...' : 'Actualizar Clave' }}
           </button>
         </div>
       </div>
     </div>
  </div>
</template>

<style scoped>
.error-message {
  color: red;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
</style>

