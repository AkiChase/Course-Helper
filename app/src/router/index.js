import {createRouter, createWebHashHistory} from 'vue-router'
import Login from "@/views/Login"
import Home from "@/views/Home"
import Course from "@/views/Course"
import HomeworkDetails from "@/views/HomeworkDetails"
import Download from "@/views/Download"

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
    },
    {
        path: '/course/:id?/:name?',
        name: 'course',
        component: Course,
    },
    {
        path: '/download',
        name: 'download',
        component: Download,
    },
    {
        path: '/homeworkDetails',
        name: 'homeworkDetails',
        component: HomeworkDetails,
    }
]

const router = createRouter({
    routes,
    history: createWebHashHistory()
})

// 暴露给api模块
window.$routerPush = router.push

export default router
