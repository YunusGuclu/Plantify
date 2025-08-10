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
        <h1>Bitkilerinize Can Verin</h1>
        <p>En etkili bitki koruma ürünleriyle hastalıklara karşı tam koruma sağlayın.</p>
      </div>
    </section>

    <!-- MAIN CONTENT -->
    <div class="product-page">
      <!-- Sidebar -->
      <aside class="sidebar">
        <h3>Kategori</h3>
        <ul>
          <li
            :class="{ active: selectedCategory === cat }"
            v-for="cat in categories"
            :key="cat"
            @click="selectCategory(cat)"
          >
            {{ translate(cat) }}
          </li>
        </ul>
      </aside>

      <!-- Ürün Kartları, Sıralama ve Sayfalama -->
      <section class="products-list">
        <!-- Sıralama Kontrolleri -->
        <div class="products-list__controls">
          <label for="sort-select" class="sort-label">Sırala:</label>
          <div class="dropdown">
            <button @click="toggleDropdown" class="dropdown__button">
              {{ currentSortLabel }}
              <i :class="dropdownOpen ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
            </button>
            <ul v-if="dropdownOpen" class="dropdown__menu">
              <li @click="changeSort('sales')">Çok Satanlar</li>
              <li @click="changeSort('price_asc')">Fiyata (Düşük→Yüksek)</li>
              <li @click="changeSort('price_desc')">Fiyata (Yüksek→Düşük)</li>
            </ul>
          </div>
        </div>

        <!-- Ürün Kartları -->
        <div class="grid">
          <div
            v-for="p in paginatedProducts"
            :key="p.id"
            class="card"
            @click="goToDetail(p)"
          >
            <div
              class="card__image"
              :style="{ backgroundImage: `url(${p.image})` }"
            ></div>
            <div class="card__body">
              <h4>{{ p.name }}</h4>
              <p class="price">₺{{ p.price.toFixed(2) }}</p>
              <button class="btn--small" @click.stop="addToCartAndAlert(p)">
                Sepete Ekle
              </button>
            </div>
          </div>
        </div>

        <!-- Sayfalama Kontrolleri -->
        <div class="pagination">
          <button @click="prevPage" :disabled="page === 1">Önceki</button>
          <button
            v-for="num in pages"
            :key="num"
            @click="goToPage(num)"
            :class="{ active: page === num }"
          >
            {{ num }}
          </button>
          <button @click="nextPage" :disabled="page === totalPages">Sonraki</button>
        </div>
      </section>
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
            <button type="submit" class="btn--small">Abone Ol</button>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCart } from '@/stores/cartStore'

const router = useRouter()
const theme = ref('light')
const { cartCount, addToCart } = useCart()
const newsletterEmail = ref('')
const products = ref([])
const categories = ref(['Tümü'])
const selectedCategory = ref('Tümü')

// Pagination
const page = ref(1)
const pageSize = 16
const totalPages = computed(() => Math.ceil(sortedProducts.value.length / pageSize))
const pages = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1))

// Sorting & dropdown
const sortOrder = ref('sales')
const dropdownOpen = ref(false)

// Category map
const categoryMap = {
  'Apple': 'Elma',
  'Blueberry': 'Yaban Mersini',
  'Cherry_(including_sour)': 'Kiraz',
  'Corn_(maize)': 'Mısır',
  'Grape': 'Üzüm',
  'Orange': 'Portakal',
  'Peach': 'Şeftali',
  'Pepper,_bell': 'Dolmalık Biber',
  'Potato': 'Patates',
  'Raspberry': 'Ahududu',
  'Soybean': 'Soya',
  'Squash': 'Kabak',
  'Strawberry': 'Çilek',
  'Tomato': 'Domates',
}
// Labels
const sortOptionsLabel = {
  sales: 'Çok Satanlar',
  price_asc: 'Fiyata (Düşük→Yüksek)',
  price_desc: 'Fiyata (Yüksek→Düşük)',
}
const currentSortLabel = computed(() => sortOptionsLabel[sortOrder.value])

// Theme toggle
function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme.value)
}

// Dropdown
function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}
function changeSort(order) {
  sortOrder.value = order
  dropdownOpen.value = false
  page.value = 1
}

// Fetch products
async function fetchProducts() {
  const res = await fetch('/api/all-products/')
  const json = await res.json()
  products.value = json.products
  const raw = Array.from(new Set(products.value.map(p => p.class_name.split('___')[0])))
  categories.value = ['Tümü', ...raw]
}

// Filtering & sorting
const sortedProducts = computed(() => {
  let list = products.value.filter(p =>
    selectedCategory.value === 'Tümü'
      ? true
      : p.class_name.split('___')[0] === selectedCategory.value
  )
  if (sortOrder.value === 'price_asc') list.sort((a, b) => a.price - b.price)
  else if (sortOrder.value === 'price_desc') list.sort((a, b) => b.price - a.price)
  else list.sort((a, b) => (b.sales || 0) - (a.sales || 0))
  return list
})

// Pagination
const paginatedProducts = computed(() =>
  sortedProducts.value.slice((page.value - 1) * pageSize, page.value * pageSize)
)
function goToPage(n) {
  page.value = n
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
function prevPage() { if (page.value > 1) page.value-- }
function nextPage() { if (page.value < totalPages.value) page.value++ }

// Cart
function addToCartAndAlert(p) {
  addToCart(p)
  alert(`${p.name} sepete eklendi!`)
}

// Category select
function selectCategory(cat) {
  selectedCategory.value = cat
  page.value = 1
}

// Translate
function translate(cat) {
  return categoryMap[cat] || cat
}

// Subscribe
function onSubscribe() {
  alert(`Teşekkürler, ${newsletterEmail.value} ile abone oldunuz!`)
  newsletterEmail.value = ''
}

// Detail navigation
function goToDetail(p) {
  router.push({ name: 'product-detail', params: { name: p.name } })
}

onMounted(fetchProducts)
</script>

<style scoped>
:root {
  --light-bg: #f0f4f8;
  --light-card: #fff;
  --light-text: #333;
  --light-accent: #2e7d32;
  --dark-bg: #121212;
  --dark-card: #1e1e1e;
  --dark-text: #eee;
  --dark-accent: #66bb6a;
  --transition: 0.4s;
  --sidebar-bg: #e8f5e9;
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

/* Tema Butonu */
.theme-toggle {
  position: fixed;
  top: 1rem;
  right: 1rem;
  background: transparent;
  border: none;
  font-size: 1.4rem;
  color: inherit;
  cursor: pointer;
  transition: transform .3s;
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
  background: url('/media/heroimage/pngtree-early-morning-pesticide-spray-for-plant-protection-in-agriculture-photo-image_32220386.jpg') center/cover no-repeat;
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

/* PRODUCT LAYOUT */
.product-page {
  display: flex;
  padding: 2rem;
  gap: 2rem;
}
.sidebar {
  width: 240px;
  background: var(--sidebar-bg);
  padding: 1rem;
  border-radius: 8px;
}
.sidebar h3 {
  margin-top: 0;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  background: #ffffff;
  color: rgb(37,65,23);
  border-radius: 4px;
  transition: background 0.3s, color 0.3s;
}
.sidebar li:hover,
.sidebar li.active {
  background: rgb(37,65,23);
  color: #ffffff;
}

/* Sıralama Kontrolleri */
.products-list__controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.sort-label {
  font-weight: 600;
}
.dropdown {
  position: relative;
}
.dropdown__button {
  padding: 0.4rem 0.8rem;
  border: 1px solid var(--light-accent);
  border-radius: 20px;
  background: none;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background var(--transition), color var(--transition);
}
.home-page.dark .dropdown__button {
  border-color: var(--dark-accent);
}
.dropdown__menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 0.5rem;
  list-style: none;
  padding: 0.5rem 0;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  z-index: 50;
  color:black;
}
.home-page.dark .dropdown__menu {
  background: var(--dark-card);
  border-color: var(--dark-accent);
}
.dropdown__menu li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  white-space: nowrap;
  transition: background .3s, color .3s;
}
.dropdown__menu li:hover {
  background: rgb(37,65,23);
  color: white;
}
.home-page.dark .dropdown__menu li:hover {
  background: var(--dark-accent);
}

/* Ürün Kartları */
.products-list {
  flex: 1;
}
.grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fill, minmax(240px,1fr));
}
.card {
  background: var(--light-card);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  transition: transform .3s, box-shadow .3s;
  cursor: pointer;
}
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}
.card__image {
  width: 100%;
  padding-top: 60%;
  background-size: cover;
  background-position: center;
}
.card__body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.card__body h4 {
  font-size: 1.1rem;
  margin: 0;
  color: var(--dark-text);
}
.price {
  font-size: 1rem;
  font-weight: 600;
  color: var(--light-accent);
  margin: 0;
}
.btn--small {
  align-self: start;
  padding: 0.6rem 1.2rem;
  background: #ffffff; color: rgb(37,65,23);
  border: none; border-radius: 8px;
  font-weight: 500; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  transition: background .3s, transform .3s, color .3s;
  cursor: pointer;
}
.btn--small:hover {
  background: rgb(37,65,23);
  color: #ffffff; transform: translateY(-2px);
}

/* Sayfalama */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 0.5rem;
}
.pagination button {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--light-accent);
  border-radius: 4px;
  cursor: pointer;
  background: none;
  transition: background var(--transition), color var(--transition);
  color:black;
}
.home-page.dark .pagination button {
  border-color: var(--dark-accent);
}
.pagination button.active {
  background: black;
  color: #fff;
}
.home-page.dark .pagination button.active {
  background: var(--dark-accent);
}
.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
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

</style>
