import { createRouter, createWebHistory } from 'vue-router';
import HomeView          from '../views/HomeView.vue';
import PlantAnalysisView from '../views/PlantAnalysisView.vue';
import ProductView       from '../views/ProductView.vue';
import BasketView        from '../views/BasketView.vue';
import ProductDetailView   from '../views/ProductDetailView.vue';

const routes = [
  { path: '/',         name: 'home',      component: HomeView },
  { path: '/analysis', name: 'analysis',  component: PlantAnalysisView },
  { path: '/products', name: 'products',  component: ProductView },
  { path: '/cart',     name: 'cart',      component: BasketView },
  { path: '/products/:name', name: 'product-detail',  component: ProductDetailView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});