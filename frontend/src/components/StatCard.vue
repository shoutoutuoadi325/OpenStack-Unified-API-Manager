<template>
  <div class="card">
    <div class="label">{{ label }}</div>
    <div class="value">{{ value }}</div>
    <div class="hint" v-if="hint">{{ hint }}</div>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  hint: String,
});
</script>

<style scoped>
.card {
  padding: 14px 16px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(42, 212, 163, 0.12), rgba(69, 160, 230, 0.08));
  border: 1px solid var(--border);
}

.label {
  color: var(--muted);
  font-size: 13px;
  margin-bottom: 6px;
}

.value {
  font-size: 28px;
  font-weight: 700;
}

.hint {
  margin-top: 6px;
  color: var(--muted);
  font-size: 12px;
}
</style>
