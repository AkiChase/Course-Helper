import axios from "axios";
import store from "@/store"


function noLoginCheck(e, reject) {
    if (e?.response?.data?.detail?.msg === '用户未登录') {
        store.dispatch('logout').then(() => {
            window.$routerPush({name: 'login'}).then(() => {
                reject('用户未登录')
            })
        })
    } else {
        reject(e.response.data.detail.msg ?? '未知错误，请求失败')
    }
}

export default {
    get(url) {
        return new Promise((resolve, reject) => {
            axios.get(url).then(res => {
                if (!res.data?.success) {
                    console.error('api get请求失败', res.data)
                    reject(res.data.detail.msg ?? '未知错误，请求失败')
                } else {
                    resolve(res.data)
                }
            }).catch(e => {
                console.error('api get请求失败', e)
                noLoginCheck(e, reject)
            })
        })
    },
    post(url, data) {
        return new Promise((resolve, reject) => {
            axios.post(url, data).then(res => {
                if (!res.data?.success) {
                    console.error('api post请求失败', res.data)
                    reject(res.data.detail.msg ?? '未知错误，请求失败')
                } else {
                    resolve(res.data)
                }
            }).catch(e => {
                console.error('api post请求失败', e)
                noLoginCheck(e, reject)
            })
        })
    }
}
