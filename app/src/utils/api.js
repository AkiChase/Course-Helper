import axios from "axios";
import store from "@/store"


function noLoginCheck(e, reject) {
    if (e?.response?.data?.detail?.msg === '用户未登录') {
        store.dispatch('logout').then(() => {
            window.$routerPush({name: 'login'}).then(() => {
                reject('用户未登录')
            })
        })
    } else if (e?.message.indexOf('timeout') > -1) reject('请求超时')
    else reject(e?.response?.data?.detail?.msg ?? '未知错误，请求失败')
}

export default {
    get(url, params = {}) {
        return new Promise((resolve, reject) => {
            if (!store.state.connectState) {
                reject('服务端未连接！')
                return
            }
            axios.get(url, {timeout: 5000, params}).then(res => {
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
            if (!store.state.connectState) {
                reject('服务端未连接！')
                return
            }
            axios.post(url, data, {timeout: 5000}).then(res => {
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
