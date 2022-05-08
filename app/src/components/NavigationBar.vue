<template>
  <div class="main" :style="`background-color: ${themeVars.primaryColor}`">
    <div class="logo">
      <img src="../assets/logo.png" alt=""/>
    </div>

    <nav-button :to="{name:'login'}">
      <settings-outline/>
    </nav-button>
    <nav-button :to="{name:'home'}">
      <settings-outline/>
    </nav-button>
    <n-switch v-model:value="darkThemeFlag" size="large" style="position: absolute; bottom: 20px">
      <template #checked-icon>
        <n-icon :component="Moon" color="#0c7a43"/>
      </template>
      <template #unchecked-icon>
        <n-icon :component="Sunny" color="#0c7a43"/>
      </template>
    </n-switch>
  </div>
</template>

<script>


import {darkTheme, NIcon, NSwitch, useThemeVars} from "naive-ui";
import Login from "@/views/Login";
import NavButton from "@/components/NavButton";
import {Moon, SettingsOutline, Sunny} from "@vicons/ionicons5";
import {useStore} from "vuex";
import {computed} from "vue";

export default {
  name: "NavigationBar",
  components: {
    Login,
    SettingsOutline, Sunny, Moon,
    NavButton, NSwitch, NIcon
  },
  setup() {
    const store = useStore()
    const themeVars = useThemeVars()
    const darkThemeFlag = computed({
      get() {
        return store.state.themeValue === 'darkTheme'
      },
      set(v) {
        store.commit('SET_THEME_VARS', {themeValue: v ? 'darkTheme' : 'default'})
      }
    })
    const theme = computed(() => store.state.themeValue === 'darkTheme' ? darkTheme : null)

    return {
      themeVars,
      darkThemeFlag,
      theme,
      Sunny, Moon
    }
  }
}
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo {
  padding: 0 10px;
}

.logo > img {
  width: 100%;
}
</style>
