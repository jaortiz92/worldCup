<script setup>
import { ref, onMounted } from 'vue';
import { useMatchesStore } from '../../stores/matches';
import { useTeamsStore } from '../../stores/teams';

const matchesStore = useMatchesStore();
const teamsStore = useTeamsStore();
const showingCreateModal = ref(false);
const editingMatch = ref(null);

const newMatch = ref({
  home_team_id: '',
  away_team_id: '',
  match_date: '',
  stage: 'Group Stage',
  status: 'pending',
});

const editData = ref({});

onMounted(async () => {
  await Promise.all([
    matchesStore.fetchMatches(),
    teamsStore.fetchTeams()
  ]);
});

const handleCreate = async () => {
   if (newMatch.value.home_team_id === newMatch.value.away_team_id) {
     alert('El equipo local y el visitante no pueden ser el mismo');
     return;
   }
  try {
    await matchesStore.createMatch(newMatch.value);
    showingCreateModal.value = false;
    newMatch.value = { home_team_id: '', away_team_id: '', match_date: '', stage: 'Group Stage', status: 'pending' };
   } catch (err) {
     alert(err.response?.data?.detail || 'Error al crear el partido');
   }
};

const startEdit = (match) => {
  editingMatch.value = match;
  editData.value = { ...match };
};

const handleUpdate = async () => {
  try {
    await matchesStore.updateMatch(editingMatch.value.id, editData.value);
    editingMatch.value = null;
   } catch (err) {
     alert(err.response?.data?.detail || 'Error al actualizar el partido');
   }
};
</script>

<template>
  <div>
     <div class="flex justify-between align-center mb-2">
       <h1>Gestionar Partidos</h1>
       <button @click="showingCreateModal = true" class="btn btn-primary">Agregar Partido</button>
     </div>
 
     <div class="card">
       <div v-if="matchesStore.loading">Cargando...</div>
      <div v-else class="table-responsive">
        <table>
           <thead>
             <tr>
               <th>Partido</th>
               <th>Fecha</th>
               <th>Estado</th>
               <th>Marcador</th>
               <th>Acciones</th>
             </tr>
           </thead>
          <tbody>
            <tr v-for="match in matchesStore.matches" :key="match.id">
              <td>{{ match.home_team?.name }} vs {{ match.away_team?.name }}</td>
              <td>{{ new Date(match.match_date).toLocaleString() }}</td>
              <td>{{ match.status }}</td>
              <td>{{ match.home_goals ?? '-' }} - {{ match.away_goals ?? '-' }}</td>
               <td>
                 <button @click="startEdit(match)" class="btn btn-primary" style="padding: 5px 10px; font-size: 0.8rem;">Editar</button>
               </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showingCreateModal" class="modal-overlay">
       <div class="modal-content card">
         <h2>Agregar Nuevo Partido</h2>
         <form @submit.prevent="handleCreate">
           <div class="form-group">
             <label>Equipo Local</label>
             <select v-model="newMatch.home_team_id" class="form-control" required>
               <option value="" disabled>Seleccione Equipo Local</option>
              <option v-for="team in teamsStore.teams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>
           <div class="form-group">
             <label>Equipo Visitante</label>
             <select v-model="newMatch.away_team_id" class="form-control" required>
               <option value="" disabled>Seleccione Equipo Visitante</option>
              <option v-for="team in teamsStore.teams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>
           <div class="form-group">
             <label>Fecha y Hora del Partido</label>
             <input v-model="newMatch.match_date" type="datetime-local" class="form-control" required />
           </div>
           <div class="form-group">
             <label>Etapa</label>
             <input v-model="newMatch.stage" type="text" class="form-control" />
           </div>
           <div class="flex justify-between align-center mt-2">
             <button type="button" @click="showingCreateModal = false" class="btn btn-danger">Cancelar</button>
             <button type="submit" class="btn btn-primary">Guardar Partido</button>
           </div>
        </form>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingMatch" class="modal-overlay">
       <div class="modal-content card">
         <h2>Editar Partido</h2>
         <form @submit.prevent="handleUpdate">
           <div class="form-group">
             <label>Goles Local</label>
             <input v-model.number="editData.home_goals" type="number" class="form-control" />
           </div>
           <div class="form-group">
             <label>Goles Visitante</label>
             <input v-model.number="editData.away_goals" type="number" class="form-control" />
           </div>
           <div class="form-group">
             <label>Estado</label>
             <select v-model="editData.status" class="form-control">
               <option value="pending">Pendiente</option>
               <option value="in_progress">En Progreso</option>
               <option value="finished">Finalizado</option>
             </select>
           </div>
           <div class="flex justify-between align-center mt-2">
             <button type="button" @click="editingMatch = null" class="btn btn-danger">Cancelar</button>
             <button type="submit" class="btn btn-primary">Actualizar Partido</button>
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
