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

    <!-- HERO PARALLAX -->
    <section class="hero">
      <div class="hero__bg"></div>
      <div class="hero__content">
        <h1>Doğayla Bütünleşin</h1>
        <p>Bitkileriniz için en saf ve yenilikçi bakım serisi.</p>
        <router-link to="/products" class="btn btn--hero">Keşfet</router-link>
      </div>
    </section>

    <!-- HASTALIK TESPİTİ -->
    <section class="detection">
      <div class="detection__overlay"></div>
      <div class="detection__content">
        <h2>Bitki Hastalıkları Tespiti</h2>
        <p>Yapay zeka destekli sistemimizle bitkinizdeki hastalığı anında keşfedin ve doğru ilacı edinin.</p>
        <router-link to="/analysis" class="btn btn--detection">Analiz Yap</router-link>
      </div>
    </section>

    <!-- POPÜLER ÜRÜNLER -->
    <section class="products">
      <h2>Popüler Ürünler</h2>
      <div class="grid">
        <div
          v-for="p in popularProducts"
          :key="p.id"
          class="card"
          @click="goToDetail(p)"
          style="cursor: pointer;"
          @mousemove="tilt($event)"
          @mouseleave="resetTilt($event)"
        >
          <div class="card__inner">
            <img :src="p.image" :alt="p.name" class="card__img" />
            <h3>{{ p.name }}</h3>
            <p class="price">{{ p.price }} ₺</p>
            <button @click.stop="addToCartAndAlert(p)" class="btn btn--small">
              Sepete Ekle
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- YENİ GELENLER -->
    <section class="products">
      <h2>Yeni Gelenler</h2>
      <div class="grid">
        <div
          v-for="p in newProducts"
          :key="p.id"
          class="card"
          @click="goToDetail(p)"
          style="cursor: pointer;"
          @mousemove="tilt($event)"
          @mouseleave="resetTilt($event)"
        >
          <div class="card__inner">
            <img :src="p.image" :alt="p.name" class="card__img" />
            <h3>{{ p.name }}</h3>
            <p class="price">{{ p.price }} ₺</p>
            <button @click.stop="addToCartAndAlert(p)" class="btn btn--small">
              Sepete Ekle
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer__container">
        <!-- Hakkımızda -->
        <div class="footer__col">
          <h4>Plantify</h4>
          <p>
            En saf ve yenilikçi bitki bakım ürünleriyle tanışın.<br />
            Misyonumuz; doğayla uyumlu, sürdürülebilir çözümler sunmak.
          </p>
        </div>
        <!-- Hızlı Linkler -->
        <div class="footer__col">
          <h4>Hızlı Linkler</h4>
          <ul>
            <li><router-link to="/">Anasayfa</router-link></li>
            <li><router-link to="/products">Ürünler</router-link></li>
            <li><router-link to="/blog">Blog</router-link></li>
            <li><router-link to="/contact">İletişim</router-link></li>
          </ul>
        </div>
        <!-- İletişim -->
        <div class="footer__col">
          <h4>İletişim</h4>
          <p>📍 İstanbul, Türkiye</p>
          <p>✉️ info@plantify.com</p>
          <p>📞 +90 (212) 123 45 67</p>
        </div>
        <!-- Bültene Abone Ol -->
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
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue';
import { useCart } from '@/stores/cartStore';

const router = useRouter()

const { cartCount, addToCart } = useCart();
const theme = ref('light');
const popularProducts = ref([]);
const newProducts = ref([]);
const newsletterEmail = ref('');

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', theme.value);
}

function goToDetail(p) {
  router.push({ name: 'product-detail', params: { name: p.name } })
}

// Tilt efektleri (mevcut)
function tilt(event) { /* … */ }
function resetTilt(event) { /* … */ }

async function fetchProducts() {
  try {
    const res = await fetch('/api/products/');
    const json = await res.json();
    popularProducts.value = json.popular;
    newProducts.value     = json.new;
  } catch (err) {
    console.error('Ürünleri alırken hata:', err);
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

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
/* TEMALAR */
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
}

.home-page {
  font-family: 'Poppins', sans-serif;
  transition: background var(--transition), color var(--transition);
}
.home-page.light {
  background: var(--light-bg);
  color: var(--light-text);
}
.home-page.dark {
  background: var(--dark-bg);
  color: var(--dark-text);
}

/* TEMA BUTONU */
.theme-toggle {
  position: fixed; top: 1rem; right: 1rem;
  background: transparent; border: none; font-size: 1.4rem;
  color: inherit; cursor: pointer;
  transition: transform .3s;
}
.theme-toggle:hover { transform: rotate(20deg); }

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
  background: url('/media/heroimage/Isik-ve-Bitkiler.jpg') center/cover no-repeat;
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
.btn--hero {
  background: var(--light-accent); color: #fff;
  padding: .75rem 2rem; border-radius: 50px;
  font-weight: 600; transition: background .3s;
}

.home-page.dark .btn--hero { background: var(--dark-accent); }
.btn--hero:hover { background: #1b5e20; }

/* HASTALIK TESPİTİ */
.detection {
  position: relative;
  margin: 4rem 2rem;
  height: 320px;
  border-radius: 16px;
  overflow: hidden;
  background: url('/media/detection-bg.jpg') center/cover no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
}
.detection__overlay {
  position: absolute;
  inset: 0;
  background: var(--bg);
  box-shadow: 0 0 10px 2px rgb(37,65,23);
  box-shadow: 0 0 10px rgb(37,65,23) inset, 0 0 2px 2px rgb(37,65,23);
}
.detection__content {
  position: relative;
  z-index: 1;
  text-align: center;
  color:  rgb(37,65,23);
  max-width: 600px;
  padding: 1rem;
}
.detection__content h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0,0,0,0.7);
}
.detection__content p {
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}
.btn--detection {
  padding: .75rem 2rem;
  font-weight: 600;
  border-radius: 50px;
  background: var(--bg);
  color: var(--light-accent);
  transition: transform .3s, background .3s;
  border:2px solid black;
}
.btn--detection:hover {
  transform: translateY(-3px);
  background: #e8f5e9;
}
.home-page.dark .detection {
  background: url('/media/detection-bg-dark.jpg') center/cover no-repeat;
}
.home-page.dark .detection__overlay {
  background: rgba(0,0,0,0.7);
}
.home-page.dark .btn--detection {
  background: var(--dark-accent);
  color: #fff;
}
.home-page.dark .btn--detection:hover {
  background: #388e3c;
}

/* ÜRÜNLER */
.products {
  padding: 3rem 2rem;
}
.products h2 {
  text-align: center; margin-bottom: 2rem; font-size: 2rem;
}
.grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
}
.card {
  perspective: 1000px;
}
.card__inner {
  background: var(--light-card);
  border-radius: 16px;
  box-shadow: 8px 8px 16px rgba(0,0,0,0.1),
              -8px -8px 16px rgba(255,255,255,0.7);
  padding: 1rem;
  text-align: center;
  transform-style: preserve-3d;
  transition: transform var(--transition), box-shadow var(--transition);
}
.home-page.dark .card__inner {
  background: var(--dark-card);
  box-shadow: 8px 8px 16px rgba(0,0,0,0.5),
              -8px -8px 16px rgba(255,255,255,0.1);
}
.card__img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 1rem;
}
.card__inner h3 {
  margin: .5rem 0;
}
.price {
  font-weight: bold;
  margin-bottom: 1rem;
  color: var(--light-accent);
}
.home-page.dark .price {
  color: var(--dark-accent);
}
.btn--small {
  padding: .5rem 1rem;
  border-radius: 50px;
  border: 2px solid currentColor;
  background: transparent;
  font-weight: 500;
  transition: background var(--transition), color var(--transition);
  cursor: pointer;
}
.btn--small:hover {
  background: currentColor;
  color: #fff;
}

/* PROFESYONEL FOOTER */

.footer {
  background: #ffffff;
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
  color: rgb(37,65,23);
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

/* BUTON RENKLERİ */
.btn,
.btn--small,
.btn--hero,
.btn--detection,
.btn--cta {
  color: rgb(37,65,23);
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
