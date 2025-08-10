<template>
  <div :class="['home-page', theme]">
    <!-- Tema Toggle -->
    <button @click="toggleTheme" class="theme-toggle">
      <i :class="theme === 'light' ? 'fas fa-moon' : 'fas fa-sun'"></i>
    </button>

    <!-- HEADER -->
    <header class="header">
      <div class="logo">🌱 Plantify</div>
      <nav class="nav">
        <router-link to="/" class="nav__link">Anasayfa</router-link>
        <router-link to="/products" class="nav__link">Ürünler</router-link>
        <router-link to="/blog" class="nav__link">Blog</router-link>
        <router-link to="/contact" class="nav__link">İletişim</router-link>
      </nav>
      <router-link to="/cart" class="cart">
        <i class="fas fa-shopping-cart"></i><span>{{ cartCount }}</span>
      </router-link>
    </header>

    <!-- HERO -->
    <section class="hero">
      <div class="hero__bg"></div>
      <div class="hero__content">
        <h1>Bitki Analizi</h1>
        <p>Fotoğrafınızı yükleyin, gerisini yapay zeka halletsin.</p>
      </div>
    </section>

    <!-- ANALİZ BÖLÜMÜ -->
    <div class="main">
      <!-- Görsel Yükleme Kartı -->
      <UploadCard
        class="analysis-card"
        :preview-url="previewUrl"
        :loading="loading"
        @file-change="onFileSelected"
        @start="startWorkflow"
      />

      <!-- Durum & Sonuç Kartı -->
      <StatusCard
        class="analysis-card"
        :status-text="statusText"
        :loading="loading"
        :result="result"
      />

      <!-- İlaç Önerileri -->
      <div
        v-if="!loading && result.pesticides && result.pesticides.length"
        class="recommendations"
      >
        <h3>Önerilen İlaçlar</h3>
        <ul class="pesticide-list">
          <li v-for="p in result.pesticides" :key="p.name" class="pesticide-card">
            <img v-if="p.image" :src="p.image" alt="" />
            <div class="details">
              <strong>{{ p.name }}</strong>
              <p>{{ p.weight_gram }} g — {{ p.price }} ₺</p>
              <small>{{ p.description }}</small>
              <!-- Sepete Ekle Butonu -->
              <button class="btn btn--small" @click="addToCartAndAlert(p)">
                Sepete Ekle
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer__container">
        <div class="footer__col">
          <h4>Plantify</h4>
          <p>
            En saf ve yenilikçi bitki bakım ürünleriyle tanışın.<br />
            Misyonumuz; doğayla uyumlu, sürdürülebilir çözümler sunmak.
          </p>
        </div>
        <div class="footer__col">
          <h4>Hızlı Linkler</h4>
          <ul>
            <li><router-link to="/">Anasayfa</router-link></li>
            <li><router-link to="/products">Ürünler</router-link></li>
            <li><router-link to="/blog">Blog</router-link></li>
            <li><router-link to="/contact">İletişim</router-link></li>
          </ul>
        </div>
        <div class="footer__col">
          <h4>İletişim</h4>
          <p>📍 İstanbul, Türkiye</p>
          <p>✉️ info@plantify.com</p>
          <p>📞 +90 (212) 123 45 67</p>
        </div>
        <div class="footer__col">
          <h4>Bültene Abone Ol</h4>
          <form @submit.prevent="onSubscribe">
            <input
              type="email"
              placeholder="E-posta adresiniz"
              v-model="newsletterEmail"
              required
            />
            <button type="submit" class="btn btn--small">Abone Ol</button>
          </form>
        </div>
      </div>
      <div class="footer__bottom">
        <div class="footer__social">
          <a href="#"><i class="fab fa-facebook-f"></i></a>
          <a href="#"><i class="fab fa-instagram"></i></a>
          <a href="#"><i class="fab fa-twitter"></i></a>
          <a href="#"><i class="fab fa-linkedin-in"></i></a>
        </div>
        <p>© 2025 Plantify. Tüm hakları saklıdır.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCart } from '@/stores/cartStore';
import UploadCard from '@/components/UploadCard.vue';
import StatusCard from '@/components/StatusCard.vue';

const { cartCount, addToCart } = useCart();
const theme           = ref('light');
const previewUrl      = ref('');
const loading         = ref(false);
const statusText      = ref('');
const result          = ref({ label: '', pesticides: [], disease: '', description: '' });
const newsletterEmail = ref('');
let poller           = null;

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', theme.value);
}

function onFileSelected(file) {
  previewUrl.value = file ? URL.createObjectURL(file) : '';
  statusText.value = '';
  result.value     = { label: '', pesticides: [], disease: '', description: '' };
}

function getCookie(name) {
  const m = document.cookie.match(new RegExp('(^|; )' + name + '=([^;]*)'));
  return m ? decodeURIComponent(m[2]) : '';
}

async function startWorkflow() {
  if (!previewUrl.value) return;
  const input = document.querySelector('input[type="file"]');
  if (!input.files.length) return;

  const fd = new FormData();
  fd.append('image', input.files[0]);

  loading.value    = true;
  statusText.value = 'Görev gönderildi. Bekleniyor…';
  result.value     = { label: '', pesticides: [], disease: '', description: '' };

  try {
    const resp1       = await fetch('/api/start/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      body: fd
    });
    const { task_id } = await resp1.json();
    statusText.value  = `Görev ID: ${task_id}`;

    poller = setInterval(async () => {
      try {
        const resp2 = await fetch(`/api/status/?task_id=${task_id}`);
        const data  = await resp2.json();

        statusText.value = `Durum: ${data.state}`;

        if (data.state === 'SUCCESS') {
          clearInterval(poller);
          loading.value = false;
          result.value  = {
            label:       data.label,
            pesticides:  data.pesticides || [],
            disease:     data.disease_info?.disease     || '',
            description: data.disease_info?.description || ''
          };
          statusText.value = `Sonuç: ${data.label}`;
        } else if (data.state === 'FAILURE') {
          clearInterval(poller);
          loading.value    = false;
          statusText.value = 'Hata oluştu!';
        }
      } catch (err) {
        console.error(err);
        clearInterval(poller);
        loading.value    = false;
        statusText.value = 'Sunucu hatası!';
      }
    }, 1000);
  } catch (err) {
    console.error(err);
    loading.value    = false;
    statusText.value = 'Gönderme hatası!';
  }
}

function addToCartAndAlert(p) {
  addToCart(p);
  alert(`${p.name} sepete eklendi!`);
}

function onSubscribe() {
  alert(`Teşekkürler, ${newsletterEmail.value} e-posta ile abone oldunuz!`);
  newsletterEmail.value = '';
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
:root {
  --light-bg: #f0f4f8;
  --light-card: #ffffff;
  --light-text: #333;
  --light-accent: #2e7d32;
  --dark-bg: #121212;
  --dark-card: #1e1e1e;
  --dark-text: #eee;
  --dark-accent: #66bb6a;
  --transition: 0.4s ease;
  --card-radius: 12px;
}

.home-page {
  font-family: 'Poppins', sans-serif;
  transition: background var(--transition), color var(--transition);
  padding-bottom: 4rem;
}
.home-page.light { background: var(--light-bg); color: var(--light-text); }
.home-page.dark  { background: var(--dark-bg); color: var(--dark-text); }

/* Tema Toggle */
.theme-toggle {
  position: fixed; top: 1rem; right: 1rem;
  background: transparent; border: none; font-size: 1.4rem;
  color: inherit; cursor: pointer;
  transition: transform 0.3s;
}
.theme-toggle:hover {
  transform: rotate(20deg);
}

/* HEADER */
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(255,255,255,0.75);
  backdrop-filter: blur(10px);
  position: sticky; top: 0; z-index: 100;
  transition: background var(--transition);
}
.home-page.dark .header {
  background: rgba(18,18,18,0.75);
}
.logo { font-size: 1.6rem; font-weight: bold; color: var(--light-accent); }
.home-page.dark .logo { color: var(--dark-accent); }
.nav__link {
  margin: 0 1rem; text-decoration: none; font-weight: 500;
  position: relative; color: inherit;
  transition: color var(--transition);
}
.nav__link::after {
  content: ''; position: absolute; bottom: -4px; left: 0; right: 0;
  height: 2px; background: currentColor;
  transform: scaleX(0); transform-origin: left;
  transition: transform var(--transition);
}
.nav__link:hover { color: var(--light-accent); }
.home-page.dark .nav__link:hover { color: var(--dark-accent); }
.nav__link:hover::after { transform: scaleX(1); }
.cart { font-size: 1.2rem; color: inherit; }

/* HERO */
.hero {
  position: relative; height: 80vh; overflow: hidden;
}
.hero__bg {
  position: absolute; inset: 0;
  background: url('/media/heroimage/a-futuristic-robot-working-in-the-field-as-a-farmer-free-photo.jpg') center/cover no-repeat;
  opacity: 0.6;
  transform: scale(1.1);
  animation: zoom 20s linear infinite;
}
@keyframes zoom {
  0% { transform: scale(1.1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1.1); }
}
.hero__content {
  position: relative; top: 50%; transform: translateY(-50%);
  text-align: center; padding: 0 1rem;
}
.hero__content h1 {
  font-size: 3rem; margin-bottom: .5rem;
  text-shadow: 0 4px 8px rgba(0,0,0,0.3);
}
.hero__content p {
  font-size: 1.2rem; margin-bottom: 1.5rem;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Main bölümü */
.main {
  display: flex; flex-wrap: wrap; justify-content: center;
  gap: 2rem; padding: 2rem 1rem 3rem;
}

/* Analysis Cards */
.analysis-card {
  width: 360px;
  background: var(--light-card);
  border-radius: var(--card-radius);
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}
.analysis-card:hover {
  transform: translateY(-5px);
}

/* İlaç Önerileri */
.recommendations {
  max-width: 420px; background: var(--light-card);
  border-radius: var(--card-radius);
  box-shadow: 0 10px 30px rgba(0,0,0,0.05); padding: 1rem;
}
.home-page.dark .recommendations {
  background: var(--dark-card);
}
.pesticide-list {
  list-style: none; padding: 0; margin: 0;
}
.pesticide-card {
  display: flex; background: var(--light-card);
  border-radius: var(--card-radius); padding: 1rem;
  align-items: center; gap: 1rem; margin-bottom: 1rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}
.pesticide-card:hover {
  transform: translateX(5px);
}
.pesticide-list img {
  border-radius: 8px; object-fit: cover; width: 80px; height: 80px;
}
.pesticide-list .details {
  font-size: 0.9rem;
}

/* PROFESYONEL FOOTER */
.footer {
  background: #ffffff; /* tamamen beyaz */
  color: #333333;
  padding: 4rem 2rem 2rem;
  font-size: 0.95rem;
  transition: background 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}
.home-page.dark .footer {
  background: var(--dark-card);
  color: var(--dark-text);
}

/* grid düzeni */
.footer__container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

/* kolon başlıkları */
.footer__col h4 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: rgb(37,65,23); /* accent başlık rengi */
}

/* liste stili */
.footer__col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer__col li {
  margin-bottom: 0.5rem;
}

/* linkler */
.footer__col a {
  color: #555555;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.3s ease;
}
.footer__col a:hover {
  color: rgb(37,65,23);
  transform: translateX(4px);
}
.home-page.dark .footer__col a:hover {
  color: var(--dark-accent);
}

/* e‑posta formu */
.footer__col form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.footer__col input[type="email"] {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: var(--card-radius);
  font-size: 0.9rem;
  transition: border-color 0.3s ease, background 0.3s ease;
}
.footer__col input[type="email"]:focus {
  outline: none;
  border-color: rgb(37,65,23);
  box-shadow: 0 0 0 2px rgba(37,65,23,0.2);
}
.home-page.dark .footer__col input[type="email"] {
  background: #333333;
  border-color: #555555;
  color: #eeeeee;
}

/* alt kısım */
.footer__bottom {
  border-top: 1px solid #eeeeee;
  padding-top: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
.footer__bottom p {
  margin: 0;
  color: #777777;
  font-size: 0.85rem;
}

/* sosyal ikonlar */
.footer__social a {
  margin: 0 0.5rem;
  font-size: 1.2rem;
  color: #555555;
  transition: transform 0.3s ease, color 0.3s ease;
}
.footer__social a:hover {
  transform: scale(1.25);
  color: rgb(37,65,23);
}
.home-page.dark .footer__social a:hover {
  color: var(--dark-accent);
}


/* Button renkleri */
.btn,
.btn--small,
.btn--hero,
.btn--detection,
.btn--cta {
  color: rgb(37,65,23);
  background-color:white;
  border-radius:30px;
  height:30px;
  
}
.btn:hover,
.btn--small:hover,
.btn--hero:hover,
.btn--detection:hover,
.btn--cta:hover {
  background-color: rgb(37,65,23);
  color: #fff;
}
.btn--small,
.btn--hero,
.btn--detection,
.btn--cta {
  border-color: rgb(37,65,23);
  cursor: pointer;
}
.btn--small:hover,
.btn--hero:hover,
.btn--detection:hover,
.btn--cta:hover {
  border-color: rgb(37,65,23);
}

/* Responsive */
@media (max-width: 600px) {
  .footer__bottom {
    text-align: center;
  }
}
</style>
