<template>
  <header class="hero">
    <h1>Bitki Hastalık Tespiti</h1>
    <p>Fotoğrafınızı yükleyin, gerisini yapay zeka halletsin!</p>
  </header>
</template>

<script setup>
// statik bir header; gerekirse title/subtitle props’u ekleyebilirsin
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: #fff;
  text-align: center;
  padding: 6rem 1rem;
  clip-path: ellipse(100% 80% at 50% 0%);
}
.hero h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: .5rem;
}
.hero p {
  font-size: 1.125rem;
  font-weight: 300;
  opacity: .9;
}
</style>
