import {createStore} from 'vuex'

export default createStore({
    state: {
        themeValue: 'default'
    },
    getters: {},
    mutations: {
        SET_THEME_VARS(state, payload) {
            state.themeValue = payload.themeValue
        }
    },
    actions: {},
    modules: {}
})
