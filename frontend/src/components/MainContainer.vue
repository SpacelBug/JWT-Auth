<template>
  <div class="work-place">
    <h3>Devices</h3>
    <div class="devices">
      <DevicePlate
          v-for="device in store.devices"
          :device="device"
      />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';

import DevicePlate from './DevicePlate.vue';

const store = useAuthStore()
</script>

<style scoped>
.work-place {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  grid-area: workPlace;
  background-color: var(--panels-color);
  width: 100%;
  height: 100%;
  border-radius: 5px;
  padding: 16px;
}

.devices {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

</style>