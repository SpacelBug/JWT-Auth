<template>
  <form class="login-form">
    <label for="login">Login</label>
    <input
        type="text"
        name="login"
        v-model="login"
    >
    <label for="password">Password</label>
    <input
        type="password"
        name="password"
        v-model="password"
    >
    <button @click.prevent="store.login({ login: login, password: password })">
      Login
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const store = useAuthStore()

const login = ref()
const password = ref()
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  grid-area: loginForm;
  background-color: var(--panels-color);
  padding: 16px;
  border-radius: 5px;
  height: 100%;
}
</style>