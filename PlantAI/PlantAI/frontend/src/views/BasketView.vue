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

    <!-- YENİ TASARIM: BASKET CONTENT -->
    <section class="basket container">
      <h2 class="basket-title">🛒 Sepetiniz</h2>

      <div v-if="cart.items.length">
        <div class="basket-grid">
          <!-- ÜRÜN KARTLARI -->
          <div class="items-list">
            <div v-for="(item, i) in cart.items" :key="i" class="item-card">
              <img v-if="item.image" :src="item.image" alt="" class="item-img" />
              <div class="item-info">
                <h3 class="item-name">{{ item.name }}</h3>
                <p class="item-weight">{{ item.weight_gram }} g</p>
                <p class="item-price">₺{{ item.price.toFixed(2) }}</p>
              </div>
              <button class="btn-remove" @click="removeItem(i)">
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>

          <!-- ÖZET KUTUSU -->
          <div class="summary-card">
            <h3 class="summary-title">Sipariş Özeti</h3>
            <div class="summary-line">
              <span>Ara Toplam</span>
              <span>₺{{ totalPrice.toFixed(2) }}</span>
            </div>
            <div class="summary-line">
              <span>KDV (18%)</span>
              <span>₺{{ (totalPrice * 0.18).toFixed(2) }}</span>
            </div>
            <div class="summary-line">
              <span>Kargo</span>
              <span>₺{{ shipping.toFixed(2) }}</span>
            </div>
            <div class="summary-total">
              <span>Genel Toplam</span>
              <strong>₺{{ (totalPrice * 1.18 + shipping).toFixed(2) }}</strong>
            </div>
            <button class="btn-checkout">Ödeme Yap</button>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <i class="fas fa-box-open empty-icon"></i>
        <p>Sepetiniz boş.</p>
        <router-link to="/products" class="btn-back">Alışverişe Devam Et</router-link>
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
import { ref } from 'vue';
import { useCart } from '@/stores/cartStore';

const { cart, cartCount, totalPrice, removeFromCart } = useCart();
const theme = ref('light');
const newsletterEmail = ref('');
const shipping = 40; // 40₺ kargo ücreti

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', theme.value);
}

function removeItem(index) {
  removeFromCart(index);
}

function onSubscribe() {
  alert(`Teşekkürler, ${newsletterEmail.value} ile abone oldunuz!`);
  newsletterEmail.value = '';
}
</script>

<style scoped>
:root {
  --light-bg: #fafafa;
  --light-card: #ffffff;
  --light-text: #333;
  --light-accent: #2e7d32;
  --dark-bg: #121212;
  --dark-card: #1e1e1e;
  --dark-text: #eee;
}

.basket-page {
  background: var(--light-bg);
  color: var(--light-text);
  min-height: 100vh;
  transition: background .3s, color .3s;
}
.basket-page.dark {
  background: var(--dark-bg);
  color: var(--dark-text);
}

/* Container */
.container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 1rem;
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

/* Grid düzeni */
.basket-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

/* Ürün kartları */
.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.item-card {
  display: flex;
  align-items: center;
  background: var(--light-card);
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.basket-page.dark .item-card {
  background: var(--dark-card);
}
.item-img {
  width: 80px; height: 80px;
  object-fit: cover;
  border-radius: 8px;
  margin-right: 1rem;
}
.item-info {
  flex: 1;
}
.item-name {
  margin: 0; font-size: 1.1rem; font-weight: 500;
}
.item-weight {
  margin: .25rem 0; color: #666;
}
.item-price {
  margin: 0; font-size: 1rem; font-weight: 600; color: var(--light-accent);
}
.btn-remove {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  color: #e74c3c;
  cursor: pointer;
  transition: color .3s;
}
.btn-remove:hover { color: #c0392b; }

/* Özet kartı (sticky) */
.summary-card {
  background: var(--light-card);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.basket-page.dark .summary-card {
  background: var(--dark-card);
}
.summary-title {
  margin: 0; font-size: 1.2rem; font-weight: 500;
  border-bottom: 1px solid #ddd; padding-bottom: .5rem;
}
.summary-line {
  display: flex; justify-content: space-between;
  font-size: .95rem; color: #555;
}
.summary-total {
  display: flex; justify-content: space-between;
  font-size: 1.1rem; font-weight: 600;
  border-top: 1px solid #ddd; padding-top: .5rem;
}
.btn-checkout {
  margin-top: 1rem;
  background: var(--light-accent);
  color: #fff;
  border: none;
  padding: .75rem;
  border-radius: 50px;
  cursor: pointer;
  transition: background .3s;
}
.btn-checkout:hover { background: #1b5e20; }

/* Boş sepet */
.empty-state {
  text-align: center; padding: 4rem 0;
}
.empty-icon {
  font-size: 4rem; color: #ccc; margin-bottom: 1rem;
}
.btn-back {
  display: inline-block; margin-top: 1rem;
  background: var(--light-accent); color: #fff;
  padding: .5rem 1rem; border-radius: 50px;
  text-decoration: none; transition: background .3s;
  background-color:white;
  color:#1b5e20;
}
.btn-back:hover { background: #1b5e20; 
color:white;}

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
</style>
