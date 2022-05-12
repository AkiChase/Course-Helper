<template>
  <div class="main">
    <n-card v-show="!loginState" hoverable="" class="card">
      <LoginForm @send-msg="sendMsg"/>
    </n-card>
    <UserInfo :words="words" :userInfo="userInfo" v-show="loginState" @send-msg="sendMsg"/>
  </div>
</template>

<script>
import {NCard, useMessage} from "naive-ui";
import {computed} from "vue";
import LoginForm from "@/components/LoginForm";
import UserInfo from "@/components/UserInfo";
import {useStore} from "vuex";

export default {
  name: "Login",
  components: {
    UserInfo, LoginForm, NCard
  },
  setup() {
    const message = useMessage()

    window.$router.beforeEach((to) => {
      if (to.name !== 'login' && !store.state.loginState) {
        message.error('请先登录！', {
          duration: 2000,
          closable: true,
          keepAliveOnHover: true
        })
        return false
      }
      return true
    })

    const store = useStore()

    const loginState = computed(() => store.state.loginState)
    const userInfo = computed(() => store.state.userInfo)

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
      loginState,
      userInfo,
      words,
      sendMsg
    }
  }
}
</script>

<style scoped>
.main {
  width: 100%;
  height: 100%;
  display: flex;
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
</style>
