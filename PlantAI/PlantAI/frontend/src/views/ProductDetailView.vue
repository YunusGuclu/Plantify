<template>
  <div class="home-page">
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

    <!-- ÜRÜN DETAYI -->
    <section class="product-detail container" v-if="product">
      <div class="detail-wrapper">
        <div class="detail-image">
          <img :src="product.image" :alt="product.name" />
        </div>
        <div class="detail-card">
          <div class="card-header">
            <span class="category-badge">{{ translateCategory(product.class_name) }}</span>
          </div>
          <h1 class="card-title">{{ product.name }}</h1>
          <p class="card-price">₺{{ product.price.toFixed(2) }}</p>
          <ul class="card-meta">
            <li><i class="fas fa-virus"></i> {{ product.disease }}</li>
            <li><i class="fas fa-weight"></i> {{ product.weight_gram }} g</li>
          </ul>
          <p class="card-description">{{ product.description }}</p>
          <div class="card-actions">
            <button class="btn btn--primary" @click="addToCartAndAlert(product)">
              <i class="fas fa-shopping-cart"></i> Sepete Ekle
            </button>
            <span class="stock" :class="{ low: product.stock < 5 }">
              Stok: {{ product.stock }}
            </span>
          </div>
        </div>
      </div>
    </section>
    <section v-else class="container">
      <p>Ürün yükleniyor veya bulunamadı.</p>
    </section>

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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCart } from '@/stores/cartStore'

const { cartCount, addToCart } = useCart()
const route            = useRoute()
const product          = ref(null)
const newsletterEmail  = ref('')

async function fetchProduct() {
  try {
    const res  = await fetch(`/api/products/${encodeURIComponent(route.params.name)}/`)
    const json = await res.json()
    product.value = json.product
  } catch (err) {
    console.error(err)
  }
}

function addToCartAndAlert(p) {
  addToCart(p)
  alert(`${p.name} sepete eklendi!`)
}

function translateCategory(class_name) {
  return class_name.split('___')[0]
}

function onSubscribe() {
  alert(`Teşekkürler, ${newsletterEmail.value} ile abone oldunuz!`)
  newsletterEmail.value = ''
}

onMounted(fetchProduct)
</script>

<style scoped>
.home-page {
  font-family: 'Poppins', sans-serif;
  background: #f0f4f8;
  color: #333;
}

/* HEADER */
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 2rem;
  background: rgba(255,255,255,0.75);
  backdrop-filter: blur(10px);
  position: sticky; top: 0; z-index: 100;
}
.logo { font-size: 1.6rem; font-weight: bold; color: rgb(37,65,23); }
.nav__link {
  margin: 0 1rem; text-decoration: none; font-weight: 500;
  position: relative; color: inherit;
}
.nav__link::after {
  content: ''; position: absolute; bottom: -4px; left: 0; right: 0;
  height: 2px; background: currentColor;
  transform: scaleX(0); transition: transform .4s ease;
}
.nav__link:hover::after { transform: scaleX(1); }

/* ÜRÜN DETAYI */
.detail-wrapper { display: flex; gap: 2rem; border-radius: 16px; box-shadow: 0 16px 40px rgba(0,0,0,0.12); }
.detail-image {
  flex: 1 1 45%; padding: 1rem; background: #fff;
  display: flex; align-items: center; justify-content: center;
}
.detail-image img {
  width: 100%; height: auto; max-height: 500px; object-fit: contain;
  transition: transform .4s;
}
.detail-image:hover img { transform: scale(1.02); }

.detail-card {
  flex: 1 1 50%; background: rgba(255,255,255,0.95);
  padding: 2.5rem; display: flex; flex-direction: column; justify-content: space-between;
}
.category-badge {
  background: #2e7d32; color: #fff;
  padding: .25rem .75rem; border-radius: 20px; font-size: .85rem; text-transform: uppercase;
}
.card-title { margin: 1rem 0 .5rem; font-size: 2.25rem; }
.card-price { font-size: 2rem; font-weight: bold; color: #2e7d32; margin-bottom: 1.5rem; }
.card-meta { list-style: none; display: flex; gap: 1.5rem; margin-bottom: 1.5rem; }
.card-meta i { margin-right: .5rem; color: #2e7d32; }
.card-description { flex-grow: 1; line-height: 1.6; margin-bottom: 2rem; }
.btn--primary {
  background: #254117; color: #fff; border: none;
  padding: .75rem 1.75rem; border-radius: 8px; font-weight: 600;
  transition: background .3s, transform .2s;
  cursor: pointer;
}
.btn--primary:hover {
  background: #fff; color: #254117; border: 1px solid #254117;
  transform: translateY(-2px);
}
.stock { font-weight: 500; }
.stock.low { color: #d32f2f; }

/* FOOTER */
.footer {
  background: #fff; color: #333;
  padding: 4rem 2rem 2rem; font-size: .95rem;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}
.footer__container {
  display: grid; grid-template-columns: repeat(auto-fit,minmax(200px,1fr)); gap: 2rem;
  margin-bottom: 2rem;
}
.footer__col h4 { margin-bottom: 1rem; font-size: 1.1rem; color: #254117; text-transform: uppercase; }
.footer__col ul { list-style: none; padding: 0; }
.footer__col a { color: #555; text-decoration: none; transition: transform .3s; }
.footer__col a:hover { color: #254117; transform: translateX(4px); }
.footer__col input {
  padding: .75rem 1rem; border: 1px solid #ddd; border-radius: 8px;
  transition: border-color .3s;
}
.footer__col input:focus { outline: none; border-color: #254117; }
.btn--small {
  margin-top: .5rem; padding: .5rem 1rem; border: 2px solid #254117;
  border-radius: 50px; background: transparent; font-weight: 500;cursor: pointer;
}
.btn--small:hover { background: #254117; color: #fff; }
.footer__bottom {
  border-top: 1px solid #eee; padding-top: 1.5rem;
  text-align: center;
}
.footer__social a { margin: 0 .5rem; font-size: 1.2rem; transition: transform .3s; }
.footer__social a:hover { transform: scale(1.25); color: #254117; }

/* Responsive */
@media (max-width: 900px) {
  .detail-wrapper { flex-direction: column; }
}
</style>
