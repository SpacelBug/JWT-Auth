<template>
  <div :class="['device', {'current-device': device.current_device}]">
    <h3>Name: {{ device.name }}</h3>
    <div class="info">
      <span><b>Agent: </b> {{ device.user_agent }}</span>
      <span><b>Last IP: </b> {{ device.last_ip }}</span>
      <span><b>Created: </b> {{ device.created_at }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps([
  'device'
])
</script>

<style scoped>

.device {
  background-color: var(--background-color);
  padding: 16px;
  border-radius: 5px;
}

.current-device {
  border: solid 2px var(--accent-color);
}

.info {
  display: flex;
  flex-direction: column;
}

</style>