<template>
  <n-config-provider abstract="" :theme="theme">
    <div class="container">
      <TopBar class="top-bar"/>
      <NavigationBar class="nav-bar"/>
      <n-message-provider>
        <n-loading-bar-provider>
          <n-dialog-provider>
            <div class="viewer">
              <router-view v-slot="{ Component }">
                <transition name="fade">
                  <keep-alive :include="keepAlive">
                    <component :is="Component"/>
                  </keep-alive>
                </transition>
              </router-view>
            </div>
          </n-dialog-provider>
        </n-loading-bar-provider>
      </n-message-provider>
    </div>
  </n-config-provider>
</template>

<script>
import TopBar from "@/components/TopBar";
import NavigationBar from "@/components/NavigationBar";
import wsHelper from "@/utils/wsHelper";
import {darkTheme, NConfigProvider, NDialogProvider, NGi, NGrid, NLoadingBarProvider, NMessageProvider} from "naive-ui";
import {computed, watch} from "vue";
import {Boot} from '@wangeditor/editor'
import attachmentModule from '@wangeditor/plugin-upload-attachment'
import {useStore} from "vuex";
import "@/style/scrollbar.css";
import "@/style/common.css"


export default {
  name: "Header",
  components: {
    NavigationBar,
    TopBar,
    NGrid, NGi, NConfigProvider, NMessageProvider, NLoadingBarProvider, NDialogProvider,
  },
  setup() {
    const store = useStore()
    const theme = computed(() => store.state.themeValue === 'darkTheme' ? darkTheme : null)

    //文件上传插件
    Boot.registerModule(attachmentModule)

    wsHelper.connect()
    wsHelper.injectCallback(
        () => store.commit('SET_CONNECT_STATE', {state: true}),
        () => store.commit('SET_CONNECT_STATE', {state: false})
    )

    store.commit('SET_DOWNLOAD_RECORDS', {
      data: window.$electron.store.get('downloadRecords', [])
    })

    window.onbeforeunload = (e) => {
      window.$electron.store.set('downloadRecords', JSON.parse(JSON.stringify((store.state.downloadRecords))))
      console.log('下载记录已保存')
    }

    watch(
        () => store.state.loginState,
        (newState, preState) => {
          if (newState === false && preState === true) {
            console.log('登出')
            window.$routerPush({name: 'login'})
          }
        }
    )

    return {
      theme,
      keepAlive: ['CourseList', 'Login', 'Course', 'HomeworkDetails', 'Download']
    }
  }
}
</script>


<style scoped>

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
