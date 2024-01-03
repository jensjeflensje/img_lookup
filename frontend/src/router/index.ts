import { createRouter, createWebHistory } from 'vue-router'
import StartView from '@/views/StartView.vue'
import DetailView from '@/views/DetailView.vue'

const routes = [
  {
    path: '',
    name: 'start',
    component: StartView,
  },
  {
    path: '/detail/:id',
    name: 'detail',
    component: DetailView,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
