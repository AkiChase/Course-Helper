import {createStore} from 'vuex'

export default createStore({
    state: {
        themeValue: 'default',
        connectState: false,
        loginState: false,
        userInfo: {
            id: null,
            name: '',
            college: ''
        },
        downloadQueue: [],
        downloadRecords: [],
        homeworkTabs: []
    },
    getters: {},
    mutations: {
        SET_THEME_VARS(state, payload) {
            state.themeValue = payload.themeValue
        },
        SET_CONNECT_STATE(state, payload) {
            state.connectState = payload.state
        },
        SET_LOGIN_STATE(state, payload) {
            state.loginState = payload.state
        },
        SET_USER_INFO(state, payload) {
            state.userInfo = payload.info
        },
        SPLICE_DOWNLOAD_QUEUE(state, payload) {
            state.downloadQueue.splice(payload.index, 1)
        },
        SPLICE_DOWNLOAD_RECORDS(state, payload) {
            if ('index' in payload) {
                state.downloadRecords.splice(payload.index, 1)
            } else {
                state.downloadRecords.splice(0) // 全部清空
            }
        },
        PUSH_DOWNLOAD_QUEUE(state, payload) {
            state.downloadQueue.push(...payload.data)
        },
        SET_DOWNLOAD_QUEUE(state, payload) {
            if ('index' in payload) {
                state.downloadQueue[payload.index] = payload.data
            } else {
                state.downloadQueue = payload.data
            }
        },
        ADD_DOWNLOAD_RECORDS(state, payload) {
            state.downloadRecords.push(...payload.data)
        },
        SET_DOWNLOAD_RECORDS(state, payload) {
            if ('index' in payload) {
                state.downloadRecords[payload.index] = payload.data
            } else {
                state.downloadRecords = payload.data
            }
        },
        ADD_HOMEWORK_TABS(state, payload) {
            state.homeworkTabs.push(payload.data)
        },
        SET_HOMEWORK_TABS(state, payload) {
            state.homeworkTabs[payload.index] = payload.data
        },
        SPLICE_HOMEWORK_TABS(state, payload) {
            if ('index' in payload) {
                state.homeworkTabs.splice(payload.index, 1)
            } else {
                state.homeworkTabs.splice(0) // 全部清空
            }
        },
    },
    actions: {
        saveLoginInfo({commit}, info) {
            commit('SET_LOGIN_STATE', {state: true})
            commit('SET_USER_INFO', {info})
        },
        logout({commit}) {
            commit('SET_LOGIN_STATE', {state: false})
            commit('SET_USER_INFO', {info: {id: null, name: '', college: ''}})
        },
        updateDownloadProgress({commit, state}, data) {
            const index = state.downloadQueue.findIndex(item => item.downloadId === data.downloadId)
            if (index === -1) { //若下载队列中无记录则忽略
                console.log('不存在下载项:', data.downloadId)
                return
            }

            let record = state.downloadQueue[index]
            if ('finished' in data) {
                commit('SPLICE_DOWNLOAD_QUEUE', {index}) //从下载队列删除
                record = {
                    state: 'finished',
                    fileName: record.fileName,
                    filePath: record.filePath,
                    fileExt: record.fileExt,
                    fileSize: record.fileSize,
                    fileSizeRaw: record.fileSizeRaw,
                    downloadId: record.downloadId,
                }
                commit('ADD_DOWNLOAD_RECORDS', {data: [record]}) // 添加到下载记录
                return record.fileName
            } else if ('error' in data) {
                commit('SPLICE_DOWNLOAD_QUEUE', {index}) //从下载队列删除
                record = {
                    state: 'error',
                    fileName: record.fileName,
                    filePath: record.filePath,
                    fileExt: record.fileExt,
                    fileSize: record.fileSize,
                    fileSizeRaw: record.fileSizeRaw,
                    downloadId: record.downloadId,
                }
                commit('ADD_DOWNLOAD_RECORDS', {data: [record]}) // 添加到下载记录
                return record.fileName
            } else {
                record.state = 'downloading'
                record = {
                    ...record,
                    ...data
                }
                commit('SET_DOWNLOAD_QUEUE', {index, data: record}) //更新下载队列中下载进度
            }
        },
        push_download_queue({commit, state}, data) {
            const newData = []
            data.forEach(item => {
                if (item.success === true) {
                    newData.push({
                        state: 'waiting',
                        fileName: item['file_name'],
                        filePath: item['file_path'],
                        fileExt: item['file_ext'],
                        fileSize: item['file_size'],
                        fileSizeRaw: item['file_size_raw'],
                        downloadId: item['download_id'],
                    })
                }
            })
            commit('PUSH_DOWNLOAD_QUEUE', {data: newData})
        },
        removeDownloadRecord({commit, state}, data) {
            if ('downloadId' in data) {
                const index = state.downloadRecords.findIndex(item => item.downloadId === data.downloadId)
                if (index === -1) {
                    console.log('不存在下载记录:', data.downloadId)
                    return
                }
                commit('SPLICE_DOWNLOAD_RECORDS', {index})
            } else {
                commit('SPLICE_DOWNLOAD_RECORDS', {})
            }
        },
        addHomeworkTabs({commit, state}, data) {
            const index = state.homeworkTabs.findIndex(item => item['hw_id'] === data['hw_id'])
            if (index === -1) {
                commit('ADD_HOMEWORK_TABS', {data})
            } else {
                console.log('已存在该课程', data['hw_id'])
            }
        },
        updateHomeworkTabs({commit, state}, {hwId, data}) {
            const index = state.homeworkTabs.findIndex(item => item['hw_id'] === hwId)
            if (index !== -1) {
                let homeworkTab = state.homeworkTabs[index]
                homeworkTab = {
                    ...homeworkTab,
                    ...data
                }
                commit('SET_HOMEWORK_TABS', {index, data: homeworkTab}) //更新下载队列中下载进度
            } else {
                console.log('未找到此id作业', hwId)
            }

        },
        removeHomeworkTabs({commit, state}, hwId) {
            const index = state.homeworkTabs.findIndex(item => item['hw_id'] === hwId)
            if (index !== -1) {
                commit('SPLICE_HOMEWORK_TABS', {index})
            }
            return index
        }
    },
    modules: {}
})
