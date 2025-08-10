<template>
  <div class="card">
    <div class="card-header">2. Durum & Sonuç</div>
    <div class="card-body">
      <!-- Spinner yalnızca işlem devam ediyorsa -->
      <div class="loader" v-if="loading"></div>

      <!-- İşlem tamamlandıysa ve result objesi geldiyse -->
      <div class="panel" v-if="!loading && result">
        <p><strong>Tahmin:</strong> {{ result.label }}</p>
        <p v-if="result.disease"><strong>Hastalık:</strong> {{ result.disease }}</p>
        <p v-if="result.description"><strong>Açıklama:</strong> {{ result.description }}</p>

        <p v-if="result.all_classes">
          <strong>Olası Sınıflar:</strong><br />
          {{ result.all_classes.join(', ') }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  loading: Boolean,
  result: {
    type: Object,
    default: () => null
  }
})
</script>

<style scoped>
.card {
  background: #fff;
  border-radius: var(--card-radius);
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  max-width: 420px;
  display: flex;
  flex-direction: column;
}
.card-header {
  background: var(--gray-bg);
  padding: 1rem;
  font-weight: 500;
  text-align: center;
  border-bottom: 1px solid #e2e8f0;
}
.card-body {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.panel {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--gray-bg);
  border-radius: var(--card-radius);
  font-size: .95rem;
}
.loader {
  margin: 2rem auto;
  width: 40px; height: 40px;
  border: 5px solid var(--gray-bg);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin .8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
