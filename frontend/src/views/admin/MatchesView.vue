<script setup>
import { ref, onMounted } from 'vue';
import { useMatchesStore } from '../../stores/matches';
import { useTeamsStore } from '../../stores/teams';
import apiClient from '../../api/client';
import { formatToLocalTime, formatToDateTimeLocal } from '../../utils/date';

const matchesStore = useMatchesStore();
const teamsStore = useTeamsStore();
const showingCreateModal = ref(false);
const editingMatch = ref(null);
const phases = ref([]);

const newMatch = ref({
  home_team_id: '',
  away_team_id: '',
  match_date: '',
  phase_id: '',
  status: 'pending',
});

const editData = ref({});

onMounted(async () => {
  try {
    await Promise.all([
      matchesStore.fetchMatches(),
      teamsStore.fetchTeams(),
      apiClient.get('/rules/multipliers')
        .then(res => {
          phases.value = res.data;
        })
        .catch(err => {
          console.error('Error loading multipliers:', err);
          // Fallback to default phases if API fails
          phases.value = [
            { id: 1, phase_name: 'Group Stage' },
            { id: 2, phase_name: 'Round of 32/16' },
            { id: 3, phase_name: 'Quarter-finals' },
            { id: 4, phase_name: 'Semi-finals' },
            { id: 5, phase_name: 'Finals' },
          ];
        })
    ]);
  } catch (err) {
    console.error('Error loading initial data:', err);
  }
});

const handleCreate = async () => {
   if (newMatch.value.home_team_id === newMatch.value.away_team_id) {
     alert('El equipo local y el visitante no pueden ser el mismo');
     return;
   }
   try {
     const date = new Date(newMatch.value.match_date);
     if (isNaN(date.getTime())) {
       alert('Por favor, ingrese una fecha válida');
       return;
     }
     const matchData = { 
       ...newMatch.value, 
       match_date: date.toISOString() 
     };
      await matchesStore.createMatch(matchData);
      showingCreateModal.value = false;
      newMatch.value = { home_team_id: '', away_team_id: '', match_date: '', phase_id: '', status: 'pending' };
    } catch (err) {
     alert(err.response?.data?.detail || 'Error al crear el partido');
   }
};

const startEdit = (match) => {
  editingMatch.value = match;
  editData.value = { ...match, match_date: formatToDateTimeLocal(match.match_date) };
};

const handleUpdate = async () => {
  try {
    const updatePayload = { ...editData.value };
    if (updatePayload.match_date) {
      updatePayload.match_date = new Date(updatePayload.match_date).toISOString();
    }
    await matchesStore.updateMatch(editingMatch.value.id, updatePayload);
    editingMatch.value = null;
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al actualizar el partido');
  }
};

const handleDelete = async (match) => {
  if (!confirm(`¿Estás seguro de que deseas eliminar el partido ${match.home_team?.name} vs ${match.away_team?.name}?`)) {
    return;
  }
  try {
    await matchesStore.deleteMatch(match.id);
    alert('Partido eliminado correctamente');
  } catch (err) {
    alert(err.response?.data?.detail || 'Error al eliminar el partido');
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
                <th>Etapa</th>
                <th>Estado</th>
                <th>Marcador</th>
                <th>Acciones</th>
              </tr>
            </thead>
           <tbody>
              <tr v-for="match in matchesStore.matches" :key="match.id">
                <td>{{ match.home_team?.name }} vs {{ match.away_team?.name }}</td>
                <td>{{ formatToLocalTime(match.match_date) }}</td>
                <td>{{ match.phase?.phase_name || 'N/A' }}</td>
                <td>{{ match.status }}</td>
                <td>{{ match.home_goals ?? '-' }} - {{ match.away_goals ?? '-' }}</td>
                <td>
                  <button @click="startEdit(match)" class="btn btn-primary" style="padding: 5px 10px; font-size: 0.8rem; margin-right: 5px;">Editar</button>
                  <button @click="handleDelete(match)" class="btn btn-danger" style="padding: 5px 10px; font-size: 0.8rem;">Eliminar</button>
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
              <select v-model="newMatch.phase_id" class="form-control" required>
                <option value="" disabled>Seleccione Etapa</option>
                <option v-for="phase in phases" :key="phase.id" :value="phase.id">
                  {{ phase.phase_name }}
                </option>
              </select>
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
              <div class="form-group">
                <label>Etapa</label>
                <select v-model="editData.phase_id" class="form-control" required>
                  <option v-for="phase in phases" :key="phase.id" :value="phase.id">
                    {{ phase.phase_name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>Fecha y Hora</label>
                <input v-model="editData.match_date" type="datetime-local" class="form-control" />
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
