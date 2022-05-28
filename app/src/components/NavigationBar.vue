<template>
  <div class="main no-select" style="background-color: #4daf7c">
    <div class="logo">
      <img class="no-drag" src="../assets/logo.png" alt=""/>
    </div>

    <nav-button :to="{name:'login'}">
      <person-circle-outline/>
    </nav-button>
    <nav-button :to="{name:'courseList'}">
      <list-outline/>
    </nav-button>
    <nav-button :to="{name:'course'}">
      <book-outline/>
    </nav-button>
    <nav-button :to="{name:'homeworkDetails'}">
      <document-text-outline/>
    </nav-button>
    <nav-button :to="{name:'download'}">
      <cloud-download-outline/>
    </nav-button>

    <n-tooltip trigger="hover">
      <template #trigger>
        <n-icon @click="devTools" class="dev-tools" size="30">
          <tool/>
        </n-icon>
      </template>
      开发者工具
    </n-tooltip>

    <n-tooltip trigger="hover">
      <template #trigger>
        <n-icon :color="connectState?'#ffffff':'#f38181'" @click="showServerModal" class="conn-state"
                size="30">
          <Link v-show="connectState"/>
          <unlink v-show="!connectState"/>
        </n-icon>
      </template>
      服务已{{ connectState ? '连接' : '断开' }}
    </n-tooltip>

    <n-switch v-model:value="darkThemeFlag" size="large" style="position: absolute; bottom: 20px">
      <template #checked-icon>
        <n-icon :component="Moon"/>
      </template>
      <template #unchecked-icon>
        <n-icon :component="Sunny"/>
      </template>
    </n-switch>

    <n-modal class="no-select" v-model:show="showModal">
      <n-card
          style="width: 600px"
          title="后端服务管理"
          :bordered="false"
          size="huge"
          role="dialog"
          aria-modal="true"
      >
        <div style="text-align: center">
          <div style="font-size: 20px; font-weight: bolder;margin-bottom: 25px">服务已{{ connectState ? '连接' : '断开' }}</div>
          <n-space :size="30" justify="center">
            <n-button @click="server('start')">启动服务</n-button>
            <n-button @click="server('stop')">停止服务</n-button>
            <n-button @click="server('restart')">重启服务</n-button>
          </n-space>
        </div>
      </n-card>
    </n-modal>

  </div>
</template>

<script>
import {NButton, NCard, NIcon, NModal, NSpace, NSwitch, NTooltip} from "naive-ui";
import Login from "@/views/Login";
import NavButton from "@/components/NavButton";
import {
  BookOutline,
  CloudDownloadOutline,
  DocumentTextOutline,
  ListOutline,
  Moon,
  PersonCircleOutline,
  Sunny
} from "@vicons/ionicons5";
import {useStore} from "vuex";
import {computed, ref} from "vue";
import {Link, Tool, Unlink} from "@vicons/tabler";

export default {
  name: "NavigationBar",
  components: {
    Login,
    Sunny, Moon, PersonCircleOutline, Link, Unlink, BookOutline, ListOutline, DocumentTextOutline, CloudDownloadOutline,
    Tool,
    NavButton, NSwitch, NIcon, NTooltip, NModal, NCard, NSpace, NButton
  },
  setup() {
    const store = useStore()
    const showModal = ref(false)

    const connectState = computed(() => store.state.connectState)

    const darkThemeFlag = computed({
      get() {
        return store.state.themeValue === 'darkTheme'
      },
      set(v) {
        store.commit('SET_THEME_VARS', {themeValue: v ? 'darkTheme' : 'default'})
      }
    })

    return {
      darkThemeFlag,
      connectState,
      showModal,
      Sunny, Moon,
      showServerModal() {
        showModal.value = true
      },
      devTools() {
        window.$electron.win.devTools()
      },
      server(state) {
        switch (state) {
          case 'start':
            window.$electron.utils.server('start')
            break
          case 'stop':
            window.$electron.utils.server('stop')
            break
          case 'restart':
            window.$electron.utils.server('restart')
            break
        }
      }
    }
  }
}
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 15px 0 0 15px;
}

.logo {
  padding: 0 10px;
}

.logo > img {
  width: 100%;
}

.conn-state {
  position: absolute;
  bottom: 60px;
  color: white;
}

.dev-tools {
  position: absolute;
  bottom: 115px;
  color: white;
}

</style>
