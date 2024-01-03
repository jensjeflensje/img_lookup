import { createApp } from 'vue'
import router from '@/router'
import App from './App.vue'
import pinia from '@/store'
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/lara-dark-green/theme.css'
import 'primeicons/primeicons.css'
import './style.css'

createApp(App)
    .use(router)
    .use(pinia)
    .use(PrimeVue)
    .mount('#app')
