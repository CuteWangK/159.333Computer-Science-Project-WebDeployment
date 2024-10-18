import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/chat/:uuid',  // Dynamic route, :uuid indicates that UUID is a dynamic parameter
        name: 'chat',
        component: HomeView,  // Continue using HomeView to display the selected chat content
        props: true  // Pass UUID as props to the component
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
