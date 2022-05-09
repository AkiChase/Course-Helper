import {createStore} from 'vuex'

export default createStore({
    state: {
        themeValue: 'default',
        connectState: false,
    },
    getters: {},
    mutations: {
        SET_THEME_VARS(state, payload) {
            state.themeValue = payload.themeValue
        },
        SET_CONNECT_STATE(state, payload) {
            state.connectState = payload.state
        }
    },
    actions: {},
    modules: {}
})
