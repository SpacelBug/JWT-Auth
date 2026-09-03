<template>
  <div :class="['token-plate', { 'active': active }]">
    {{ token.id }}
    <p>Remaining time: {{ remainingTime }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  token: Object,
  active: Boolean
})

const remainingTime = computed(() => {
  let remainingTimeMs = new Date(props.token.expires_at).getTime() - Date.now()

  if (remainingTimeMs < 0) {
    return "expired"
  }

  const seconds = Math.floor((remainingTimeMs / 1000) % 60).toString();
  const minutes = Math.floor((remainingTimeMs / (1000 * 60)) % 60).toString();
  const hours = Math.floor((remainingTimeMs) % 24).toString();

  return `${hours.padStart(2, "0")}:${minutes.padStart(2, "0")}:${seconds.padStart(2, "0")}`
})
</script>

<style scoped>
.token-plate {
  box-sizing: border-box;
  height: 100px;
  width: 150px;
  padding: 16px;
  border-radius: 10px;
  overflow: hidden;
  background-color: var(--background-color);
}

.active {
  border: solid var(--accent-color) 2px;
}
</style>