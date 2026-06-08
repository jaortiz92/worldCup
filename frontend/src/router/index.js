import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import PredictionView from '../views/PredictionView.vue';
import ProfileView from '../views/ProfileView.vue';
import MatchPredictionsView from '../views/MatchPredictionsView.vue';
import MatchesAdminView from '../views/admin/MatchesView.vue';
import UsersAdminView from '../views/admin/UsersView.vue';
import RulesAdminView from '../views/admin/RulesView.vue';
import TeamsAdminView from '../views/admin/TeamsView.vue';

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { 
    path: '/', 
    name: 'Home', 
    component: HomeView, 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/predict/:id', 
    name: 'Predict', 
    component: PredictionView, 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/profile', 
    name: 'Profile', 
    component: ProfileView, 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/predictions-match/:id', 
    name: 'MatchPredictions', 
    component: MatchPredictionsView, 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/admin/matches', 
    name: 'AdminMatches', 
    component: MatchesAdminView, 
    meta: { requiresAuth: true, requiresAdmin: true } 
  },
  { 
    path: '/admin/users', 
    name: 'AdminUsers', 
    component: UsersAdminView, 
    meta: { requiresAuth: true, requiresAdmin: true } 
  },
  { 
    path: '/admin/rules', 
    name: 'AdminRules', 
    component: RulesAdminView, 
    meta: { requiresAuth: true, requiresAdmin: true } 
  },
  { 
    path: '/admin/teams', 
    name: 'AdminTeams', 
    component: TeamsAdminView, 
    meta: { requiresAuth: true, requiresAdmin: true } 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/');
  } else {
    next();
  }
});

export default router;
