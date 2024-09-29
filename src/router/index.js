import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/:uuid', // 动态路由
    name: 'chat',
    component: HomeView, // 使用新的视图组件
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
