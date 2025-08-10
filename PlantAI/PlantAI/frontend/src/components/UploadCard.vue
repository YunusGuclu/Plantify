<template>
  <div class="card">
    <div class="card-header">1. Görsel Yükle</div>
    <div class="card-body">
      <!-- Input tüm alanı kaplasın, label’e tıkla yeter -->
      <label class="upload-wrapper">
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="onFileChange"
        />
        <i class="fas fa-camera icon"></i>
        <p>Bir resim seçin veya sürükleyin</p>
      </label>

      <!-- Önizleme varsa göster -->
      <img
        v-if="previewUrl"
        :src="previewUrl"
        class="preview"
        alt="Önizleme"
      />

      <button
        class="btn"
        :disabled="!previewUrl || loading"
        @click="$emit('start')"
      >
        {{ loading ? 'Bekleniyor…' : 'Analize Başla' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  previewUrl: String,
  loading:    Boolean
})
const emit = defineEmits(['file-change','start'])

function onFileChange(e) {
  emit('file-change', e.target.files[0] || null)
}
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
  display: flex;
  flex-direction: column;
  flex: 1;
}
.upload-wrapper {
  position: relative;
  border: 2px dashed #cbd5e0;
  border-radius: var(--card-radius);
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: border-color var(--transition), background var(--transition);
}
.upload-wrapper:hover {
  border-color: var(--primary-light);
  background: #edf7f1;
}
.upload-wrapper input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}
.icon {
  font-size: 2rem;
  color: var(--primary-light);
  margin-bottom: .5rem;
}
.preview {
  margin-top: 1rem;
  max-height: 180px;
  border-radius: var(--card-radius);
  object-fit: contain;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.btn {
  margin-top: auto;
  padding: .75rem;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: var(--card-radius);
  font-weight: 500;
  cursor: pointer;
  transition: background var(--transition), transform var(--transition);
}
.btn:disabled {
  opacity: .6;
  cursor: not-allowed;
}
.btn:hover:not(:disabled) {
  background: var(--primary-light);
  transform: translateY(-2px);
}
</style>
