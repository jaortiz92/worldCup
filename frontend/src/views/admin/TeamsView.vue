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
    alert(err.response?.data?.detail || 'Failed to create team');
  }
};

const handleDelete = async (id) => {
  if (confirm('Are you sure you want to delete this team? Matches associated with this team might be affected.')) {
    try {
      await teamsStore.deleteTeam(id);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete team');
    }
  }
};
</script>

<template>
  <div>
    <div class="flex justify-between align-center mb-2">
      <h1>Manage Teams</h1>
      <button @click="showingCreateModal = true" class="btn btn-primary">Add Team</button>
    </div>

    <div class="card">
      <div v-if="teamsStore.loading">Loading teams...</div>
      <div v-else class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>ISO Code</th>
              <th>Group</th>
              <th>Flag</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="team in teamsStore.teams" :key="team.id">
              <td><strong>{{ team.name }}</strong></td>
              <td>{{ team.code_iso }}</td>
              <td>{{ team.groups }}</td>
              <td>
                <img v-if="team.flag_url" :src="team.flag_url" alt="Flag" style="width: 30px; height: auto;" />
                <span v-else>No flag</span>
              </td>
              <td>
                <button @click="handleDelete(team.id)" class="btn btn-danger" style="padding: 5px 10px; font-size: 0.8rem;">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showingCreateModal" class="modal-overlay">
      <div class="modal-content card">
        <h2>Add New Team</h2>
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>Team Name</label>
            <input v-model="newTeam.name" type="text" class="form-control" required />
          </div>
          <div class="form-group">
            <label>ISO Code (e.g. ARG)</label>
            <input v-model="newTeam.code_iso" type="text" class="form-control" />
          </div>
          <div class="form-group">
            <label>Group (e.g. Group A)</label>
            <input v-model="newTeam.groups" type="text" class="form-control" />
          </div>
          <div class="form-group">
            <label>Flag URL</label>
            <input v-model="newTeam.flag_url" type="url" class="form-control" />
          </div>
          <div class="flex justify-between align-center mt-2">
            <button type="button" @click="showingCreateModal = false" class="btn btn-danger">Cancel</button>
            <button type="submit" class="btn btn-primary">Save Team</button>
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
