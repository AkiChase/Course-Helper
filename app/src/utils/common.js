export default {
    sendMsg(message, text, type = 'default', duration = 2500, otherOptions = {}) {
        return message.create(text, {
            type,
            duration,
            closable: true,
            keepAliveOnHover: true,
            ...otherOptions
        })
    },
    showLoading(loadingFlag) {
        loadingFlag.value = true
    },
    hideLoading(loadingFlag) {
        loadingFlag.value = false
    }
}
