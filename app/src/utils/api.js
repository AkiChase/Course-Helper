import axios from "axios";

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
                reject(e.response.data.detail.msg ?? '未知错误，请求失败')
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
                reject(e.response.data.detail.msg ?? '未知错误，请求失败')
            })
        })
    }
}
