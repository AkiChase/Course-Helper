<template>
  <div class="main" style="background-color: #4daf7c">
    <div class="logo">
      <img src="../assets/logo.png" alt=""/>
    </div>

    <nav-button :to="{name:'login'}">
      <person-circle-outline/>
    </nav-button>
    <nav-button :to="{name:'home'}">
      <book-outline/>
    </nav-button>

    <n-icon v-show="connectState" title="服务已连接" class="conn-state" size="30">
      <Link/>
    </n-icon>

    <n-icon v-show="!connectState" title="服务已断开" class="conn-state" size="30">
      <unlink/>
    </n-icon>

    <n-switch v-model:value="darkThemeFlag" size="large" style="position: absolute; bottom: 20px">
      <template #checked-icon>
        <n-icon :component="Moon"/>
      </template>
      <template #unchecked-icon>
        <n-icon :component="Sunny"/>
      </template>
    </n-switch>
  </div>
</template>

<script>
import {NIcon, NSwitch} from "naive-ui";
import Login from "@/views/Login";
import NavButton from "@/components/NavButton";
import {Moon, Sunny, PersonCircleOutline, BookOutline} from "@vicons/ionicons5";
import {useStore} from "vuex";
import {computed} from "vue";
import {Link, Unlink} from "@vicons/tabler";

export default {
  name: "NavigationBar",
  components: {
    Login,
    Sunny, Moon, PersonCircleOutline, Link, Unlink, BookOutline,
    NavButton, NSwitch, NIcon
  },
  setup() {
    const store = useStore()

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

.conn-state[title='服务已断开'] {
  color: #f38181;
}

</style>
