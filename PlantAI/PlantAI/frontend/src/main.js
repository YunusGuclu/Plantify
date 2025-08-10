// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Global CSS
import './assets/css/variables.css'

// FontAwesome
import '@fortawesome/fontawesome-free/css/all.min.css'
import '@fortawesome/fontawesome-free/js/all.min.js'

createApp(App)
  .use(router)
  .mount('#app')
