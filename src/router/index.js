import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/chat/:uuid',  // 动态路由，:uuid 表示 UUID 是动态参数
    name: 'chat',
    component: HomeView,  // 继续使用 HomeView，显示选中的聊天内容
    props: true  // 将 UUID 作为 props 传递给组件
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
