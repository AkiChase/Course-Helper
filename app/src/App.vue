<template>
  <n-config-provider abstract="" :theme="theme">
    <div class="container">
      <TopBar class="top-bar"/>
      <NavigationBar class="nav-bar"/>
      <n-message-provider>
        <div class="viewer">
          <router-view v-slot="{ Component }">
            <transition name="fade">
              <keep-alive :include="keepAlive">
                <component :is="Component"/>
              </keep-alive>
            </transition>
          </router-view>
        </div>
      </n-message-provider>
    </div>
  </n-config-provider>
</template>

<script>
import TopBar from "@/components/TopBar";
import NavigationBar from "@/components/NavigationBar";
import {NGrid, NGi, darkTheme, NConfigProvider, NMessageProvider, useMessage} from "naive-ui";
import {computed} from "vue";
import {useStore} from "vuex";


export default {
  name: "Header",
  components: {
    NavigationBar,
    TopBar,
    NGrid, NGi, NConfigProvider, NMessageProvider
  },
  setup() {
    const store = useStore()
    const theme = computed(() => store.state.themeValue === 'darkTheme' ? darkTheme : null)
    window.$ws.connect()
    window.$ws.injectCallback(
        () => store.commit('SET_CONNECT_STATE', {state: true}),
        () => store.commit('SET_CONNECT_STATE', {state: false})
    )

    return {
      theme,
      keepAlive: ['Home', 'Login']
    }
  }
}
</script>


<style scoped>
::-webkit-scrollbar {
  display: none;
}

.container {
  display: grid;
  height: 100%;
  width: 100%;
  grid-template-rows: auto 1fr;
  grid-template-columns: 75px 1fr;
  background-image: url("./assets/girl.jpg");
  background-position: center;
  background-size: cover;
  border-radius: 15px;
}

.viewer {
  background-color: rgba(255, 255, 255, 0.6);
  border-bottom-right-radius: 15px;
  overflow-y: scroll;
}

.top-bar {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: rgba(255, 255, 255, 0.6);
}

.nav-bar {
  grid-row-start: 1;
  grid-row-end: 3;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
