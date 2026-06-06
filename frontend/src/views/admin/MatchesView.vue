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
    alert('Home and away teams cannot be the same');
    return;
  }
  try {
    await matchesStore.createMatch(newMatch.value);
    showingCreateModal.value = false;
    newMatch.value = { home_team_id: '', away_team_id: '', match_date: '', stage: 'Group Stage', status: 'pending' };
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to create match');
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
    alert(err.response?.data?.detail || 'Failed to update match');
  }
};
</script>

<template>
  <div>
    <div class="flex justify-between align-center mb-2">
      <h1>Manage Matches</h1>
      <button @click="showingCreateModal = true" class="btn btn-primary">Add Match</button>
    </div>

    <div class="card">
      <div v-if="matchesStore.loading">Loading...</div>
      <div v-else class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Match</th>
              <th>Date</th>
              <th>Status</th>
              <th>Score</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="match in matchesStore.matches" :key="match.id">
              <td>{{ match.home_team?.name }} vs {{ match.away_team?.name }}</td>
              <td>{{ new Date(match.match_date).toLocaleString() }}</td>
              <td>{{ match.status }}</td>
              <td>{{ match.home_goals ?? '-' }} - {{ match.away_goals ?? '-' }}</td>
              <td>
                <button @click="startEdit(match)" class="btn btn-primary" style="padding: 5px 10px; font-size: 0.8rem;">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showingCreateModal" class="modal-overlay">
      <div class="modal-content card">
        <h2>Add New Match</h2>
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>Home Team</label>
            <select v-model="newMatch.home_team_id" class="form-control" required>
              <option value="" disabled>Select Home Team</option>
              <option v-for="team in teamsStore.teams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Away Team</label>
            <select v-model="newMatch.away_team_id" class="form-control" required>
              <option value="" disabled>Select Away Team</option>
              <option v-for="team in teamsStore.teams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Match Date & Time</label>
            <input v-model="newMatch.match_date" type="datetime-local" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Stage</label>
            <input v-model="newMatch.stage" type="text" class="form-control" />
          </div>
          <div class="flex justify-between align-center mt-2">
            <button type="button" @click="showingCreateModal = false" class="btn btn-danger">Cancel</button>
            <button type="submit" class="btn btn-primary">Save Match</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingMatch" class="modal-overlay">
      <div class="modal-content card">
        <h2>Edit Match</h2>
        <form @submit.prevent="handleUpdate">
          <div class="form-group">
            <label>Home Goals</label>
            <input v-model.number="editData.home_goals" type="number" class="form-control" />
          </div>
          <div class="form-group">
            <label>Away Goals</label>
            <input v-model.number="editData.away_goals" type="number" class="form-control" />
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="editData.status" class="form-control">
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="finished">Finished</option>
            </select>
          </div>
          <div class="flex justify-between align-center mt-2">
            <button type="button" @click="editingMatch = null" class="btn btn-danger">Cancel</button>
            <button type="submit" class="btn btn-primary">Update Match</button>
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
