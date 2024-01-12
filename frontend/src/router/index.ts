import {createRouter, createWebHistory} from 'vue-router'
import StartView from '@/views/StartView.vue'
import DetailView from '@/views/DetailView.vue'
import NotFoundView from "@/views/NotFoundView.vue";

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
  {
    path: '/notfound',
    name: 'notfound',
    component: NotFoundView,
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
