<script setup>
import { ref, onMounted } from 'vue';
import { useTeamsStore } from '../../stores/teams';

const teamsStore = useTeamsStore();
const showingCreateModal = ref(false);

const newTeam = ref({
  name: '',
  flag_url: '',
  code_iso: '',
  groups: '',
});

onMounted(() => {
  teamsStore.fetchTeams();
});

const handleCreate = async () => {
  try {
    await teamsStore.createTeam(newTeam.value);
    showingCreateModal.value = false;
    newTeam.value = { name: '', flag_url: '', code_iso: '', groups: '' };
   } catch (err) {
     alert(err.response?.data?.detail || 'Error al crear el equipo');
   }
};

 const handleDelete = async (id) => {
   if (confirm('¿Está seguro de que desea eliminar este equipo? Los partidos asociados podrían verse afectados.')) {
     try {
      await teamsStore.deleteTeam(id);
   } catch (err) {
     alert(err.response?.data?.detail || 'Error al eliminar el equipo');
   }
  }
};
</script>

<template>
  <div>
     <div class="flex justify-between align-center mb-2">
       <h1>Gestionar Equipos</h1>
       <button @click="showingCreateModal = true" class="btn btn-primary">Agregar Equipo</button>
     </div>
 
     <div class="card">
       <div v-if="teamsStore.loading">Cargando equipos...</div>
      <div v-else class="table-responsive">
        <table>
           <thead>
             <tr>
               <th>Nombre</th>
               <th>Código ISO</th>
               <th>Grupo</th>
               <th>Bandera</th>
               <th>Acciones</th>
             </tr>
           </thead>
          <tbody>
            <tr v-for="team in teamsStore.teams" :key="team.id">
              <td><strong>{{ team.name }}</strong></td>
              <td>{{ team.code_iso }}</td>
              <td>{{ team.groups }}</td>
              <td>
                <img v-if="team.flag_url" :src="team.flag_url" alt="Flag" style="width: 30px; height: auto;" />
                 <span v-else>Sin bandera</span>
              </td>
               <td>
                 <button @click="handleDelete(team.id)" class="btn btn-danger" style="padding: 5px 10px; font-size: 0.8rem;">Eliminar</button>
               </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showingCreateModal" class="modal-overlay">
       <div class="modal-content card">
         <h2>Agregar Nuevo Equipo</h2>
         <form @submit.prevent="handleCreate">
           <div class="form-group">
             <label>Nombre del Equipo</label>
             <input v-model="newTeam.name" type="text" class="form-control" required />
           </div>
           <div class="form-group">
             <label>Código ISO (ej. COL)</label>
             <input v-model="newTeam.code_iso" type="text" class="form-control" />
           </div>
           <div class="form-group">
             <label>Grupo (ej. Grupo A)</label>
             <input v-model="newTeam.groups" type="text" class="form-control" />
           </div>
           <div class="form-group">
             <label>URL de la Bandera</label>
             <input v-model="newTeam.flag_url" type="url" class="form-control" />
           </div>
           <div class="flex justify-between align-center mt-2">
             <button type="button" @click="showingCreateModal = false" class="btn btn-danger">Cancelar</button>
             <button type="submit" class="btn btn-primary">Guardar Equipo</button>
           </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  width: 400px;
  max-width: 90%;
}
</style>
