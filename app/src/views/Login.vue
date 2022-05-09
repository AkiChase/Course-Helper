<template>
  <div class="main">
    <n-card v-show="!loginState" hoverable="" class="card">
      <n-spin :show="loadingFlag">
        <LoginForm @send-msg="sendMsg" @loading-state="changeLoadingState"/>
      </n-spin>
    </n-card>
    <div class="after-login" v-show="loginState">
      <n-button @click="logout" class="logout" circle="">
        <template #icon>
          <n-icon>
            <log-out-outline/>
          </n-icon>
        </template>
      </n-button>
      <div class="user-info">
        <div>
          <div>姓名:</div>
          <div class="name">{{ userInfo.name }}</div>
        </div>
        <div>
          <div>学号:</div>
          <div>{{ userInfo.id }}</div>
        </div>
        <div>
          <div>学院:</div>
          <div>{{ userInfo.college }}</div>
        </div>
      </div>
      <div class="words">
        <span v-for="p in words">
          {{ p }}
        </span>
      </div>

    </div>
  </div>
</template>

<script>
import {NButton, NCard, NIcon, NSpin, useMessage} from "naive-ui";
import {computed, ref} from "vue";
import LoginForm from "@/components/LoginForm";
import {useStore} from "vuex";
import {LogOutOutline} from "@vicons/ionicons5";
import axios from "axios";

export default {
  name: "Login",
  components: {
    LoginForm, NSpin, NCard, NButton, NIcon, LogOutOutline
  },
  setup() {
    const message = useMessage()
    const store = useStore()

    const loginState = computed(() => store.state.loginState)
    const userInfo = computed(() => store.state.userInfo)

    const loadingFlag = ref(false)

    const words = `
你要做一个不动声色的大人了。
不准情绪化，不准偷偷想念，不准回头看。
去过自己另外的生活。
你要听话，不是所有的鱼都会生活在同一片海里。
——村上春树`.trim().split('\n')

    function sendMsg(msg, type = 'default', duration = 2500, otherOptions = {}) {
      message.create(msg, {
        type,
        duration,
        closable: true,
        keepAliveOnHover: true,
        ...otherOptions
      })
    }

    return {
      loadingFlag,
      loginState,
      userInfo,
      words,
      sendMsg,
      changeLoadingState(state) {
        loadingFlag.value = state
      },
      logout() {
        axios.get('http://127.0.0.1:6498/user/logout').then((res) => {
          if (res.data?.success) {
            sendMsg('msg' in res.data ? res.data.msg : '退出成功！', 'success')
            store.dispatch('logout')
          } else {
            sendMsg('未知错误，退出失败', 'error')
          }
        }).catch((err) => {
          sendMsg('msg' in err.response.data?.detail ? err.response.data.detail.msg : '未知错误，退出失败', 'error')
          loadingFlag.value = false
        })
      }
    }
  }
}
</script>

<style scoped>
.main {
  width: 100%;
  height: 100%;
  display: flex !important;
  justify-content: center;
  align-items: center;
  background-size: cover;
}

.card {
  width: 70%;
  padding: 15px 10%;
  border-radius: 25px;
  border: 2px #eee solid;
  background-color: rgba(255, 255, 255, 0.9);
}

.after-login {
  border: 5px #eee dashed;
  width: 50%;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 5% 10%;
  border-radius: 15px;
  font-size: 18px;
  position: relative;
}

.logout {
  position: absolute;
  right: 15px;
  top: 15px;
}

.user-info > div {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.user-info > div > div:nth-child(1) {
  font-weight: bold;
}

.words {
  display: flex;
  flex-direction: column;
  border-top: 1px #eee solid;
  margin-top: 25px;
  padding-top: 25px;
}

.words > span {
  font-size: 14px;
  text-align: center;
}

.words > span:last-child {
  font-size: 12px;
  font-weight: bold;
  text-align: right;
  margin-top: 15px;
}

</style>
