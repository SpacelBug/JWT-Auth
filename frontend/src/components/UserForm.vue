<template>
  <div class="user-form">
    <div class="data">
      <h2>User data</h2>
      <span v-for="value, key in store.user">
        <b>{{ key }}: </b>{{ value }}
      </span>
    </div>
    <div class="logout-buttons">
      <button @click="store.logout()">Logout</button>
      <button @click="store.logoutAll()">Logout All</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
const store = useAuthStore()
</script>

<style scoped>
.user-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  grid-area: loginForm;
  background-color: var(--panels-color);
  padding: 16px;
  border-radius: 5px;
  height: 100%;
}

.data {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.logout-buttons {
  display: flex;
  gap: 16px;
}

button {
  width: 100%;
}
</style>