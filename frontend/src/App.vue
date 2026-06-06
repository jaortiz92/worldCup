<script setup>
import NavBar from './components/NavBar.vue';
</script>

<template>
  <div id="app">
    <NavBar />
    
    <main class="container mt-2">
      <router-view />
    </main>
  </div>
</template>
