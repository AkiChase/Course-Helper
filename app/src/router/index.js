import {createRouter, createWebHashHistory} from 'vue-router'
import Login from "@/views/Login";

const routes = [
    {
        path: '/',
        name: 'login',
        component: Login
    },
]

const router = createRouter({
    routes,
    history: createWebHashHistory()
})

export default router
