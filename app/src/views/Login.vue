<template>
  <div>
    <h1>登录页面</h1>
    <n-button @click="changeTheme">切换</n-button>
  </div>
</template>

<script>
import {NButton, useThemeVars} from "naive-ui";
import {useStore} from "vuex";
import {computed} from "vue";

export default {
  name: "Login",
  components: {
    NButton
  },
  setup() {
    const store = useStore()
    const themeVars = useThemeVars()

    function changeTheme() {
      store.commit('SET_THEME_VARS', {themeValue: darkThemeFlag.value ? 'default' : 'darkTheme'})
    }

    const darkThemeFlag = computed(() => store.state.themeValue === 'darkTheme')

    return {
      changeTheme,
      darkThemeFlag,
      themeVars,
    }
  }
}
</script>

<style scoped>

</style>
