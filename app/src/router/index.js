import {createRouter, createWebHashHistory} from 'vue-router'
import Login from "@/views/Login";
import Home from "@/views/Home"

const routes = [
    {
        path: '/',
        name: 'login',
        component: Login
    },
    {
        path: '/home',
        name: 'home',
        component: Home
    }
]

const router = createRouter({
    routes,
    history: createWebHashHistory()
})

export default router
