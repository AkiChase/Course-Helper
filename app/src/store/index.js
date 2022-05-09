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
        }
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
        }
    },
    actions: {
        saveLoginInfo({commit}, info) {
            commit('SET_LOGIN_STATE', {state: true})
            commit('SET_USER_INFO', {info})
        },
        logout({commit}) {
            commit('SET_LOGIN_STATE', {state: false})
            commit('SET_USER_INFO', {info: {id: null, name: '', college: ''}})
        }
    },
    modules: {}
})
