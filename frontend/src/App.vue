<template>
  <div class="main-box">
    <div class="left-bar">
      <h1>Auth Service</h1>

      <LoginForm v-if="!store.isAuthorized" />
      <UserForm v-else />
    </div>

    <MainContainer v-if="store.isAuthorized" />
  </div>
</template>

<script setup>
import { onMounted, ref, defineComponent } from 'vue';
import { useAuthStore } from './stores/auth';

import LoginForm from './components/LoginForm.vue';
import UserForm from './components/UserForm.vue';
import MainContainer from './components/MainContainer.vue';

const store = useAuthStore()

onMounted(async () => {
  if (store.isAuthorized) {
    await store.getUser()
    await store.getDevices()
    await store.getTokens()
  }
})

</script>

<style scoped>
.main-box {
  box-sizing: border-box;
  display: flex;
  height: 100vh;
  width: 100vw;
  gap: 32px;
  padding: 32px;
}

.left-bar {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>
