<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../../api/client';

const rules = ref([]);
const loading = ref(false);
const showingCreateModal = ref(false);
const editingRule = ref(null);

const form = ref({
  rule_name: '',
  correct_score_points: 5,
  correct_winner_points: 2,
  correct_home_goals_points: 1,
  correct_away_goals_points: 1,
  is_active: false,
});

const fetchRules = async () => {
  loading.value = true;
  try {
    const response = await apiClient.get('/rules/');
    rules.value = response.data;
  } catch (err) {
    alert('Failed to fetch rules');
  } finally {
    loading.value = false;
  }
};

const handleSaveRule = async () => {
  try {
    if (editingRule.value) {
      await apiClient.patch(`/rules/${editingRule.value.id}`, form.value);
    } else {
      await apiClient.post('/rules/', form.value);
    }
    await fetchRules();
    showingCreateModal.value = false;
    editingRule.value = null;
    form.value = { 
      rule_name: '', 
      correct_score_points: 5, 
      correct_winner_points: 2, 
      correct_home_goals_points: 1, 
      correct_away_goals_points: 1, 
      is_active: false 
    };
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to save rule');
  }
};

const startEdit = (rule) => {
  console.log('Starting edit for rule:', rule.id);
  editingRule.value = rule;
  form.value = { ...rule };
  showingCreateModal.value = true;
};


const openCreateModal = () => {
  console.log('Opening create modal...');
  editingRule.value = null;
  form.value = { 
    rule_name: '', 
    correct_score_points: 5, 
    correct_winner_points: 2, 
    correct_home_goals_points: 1, 
    correct_away_goals_points: 1, 
    is_active: false 
  };
  showingCreateModal.value = true;
};

onMounted(fetchRules);
</script>

<template>
  <div>
    <div class="flex justify-between align-center mb-2">
      <h1>Scoring Rules</h1>
      <button @click="openCreateModal" class="btn btn-primary">Add Rule</button>
    </div>

    <div class="card">
      <div v-if="loading">Loading...</div>
      <div v-else class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Rule Name</th>
              <th>Exact Score</th>
              <th>Winner</th>
              <th>Home Goals</th>
              <th>Away Goals</th>
              <th>Active</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rule in rules" :key="rule.id">
              <td>{{ rule.rule_name }}</td>
              <td>{{ rule.correct_score_points }}</td>
              <td>{{ rule.correct_winner_points }}</td>
              <td>{{ rule.correct_home_goals_points }}</td>
              <td>{{ rule.correct_away_goals_points }}</td>
              <td>{{ rule.is_active ? '✅' : '❌' }}</td>
              <td>
                <button @click="startEdit(rule)" class="btn btn-primary" style="padding: 5px 10px; font-size: 0.8rem;">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showingCreateModal" class="modal-overlay">
      <div class="modal-content card">
        <h2>{{ editingRule ? 'Edit' : 'Create' }} Scoring Rule</h2>
        <form @submit.prevent="handleSaveRule">
          <div class="form-group">
            <label>Rule Name</label>
            <input v-model="form.rule_name" type="text" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Points for Exact Score</label>
            <input v-model.number="form.correct_score_points" type="number" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Points for Correct Winner/Draw</label>
            <input v-model.number="form.correct_winner_points" type="number" class="form-//control" required />
          </div>
          <div class="form-group">
            <label>Points for Correct Home Goals</label>
            <input v-model.number="form.correct_home_goals_points" type="number" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Points for Correct Away Goals</label>
            <input v-model.number="form.correct_away_goals_points" type="number" class="form-control" required />
          </div>
          <div class="form-group">
            <label>
              <input type="checkbox" v-model="form.is_active" />
              Make Active
            </label>
          </div>
          <div class="flex justify-between align-center mt-2">
            <button type="button" @click="showingCreateModal = false" class="btn btn-danger">Cancel</button>
            <button type="submit" class="btn btn-primary">Save Rule</button>
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
