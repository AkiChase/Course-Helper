<template>
  <n-spin class="after-login" :show="loadingFlag">
    <n-button @click="logout" class="logout" circle="">
      <template #icon>
        <n-icon>
          <log-out-outline/>
        </n-icon>
      </template>
    </n-button>
    <div class="user-info">
      <h2 style="text-align: center">登录成功</h2>
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
  </n-spin>
</template>

<script>
import axios from "axios";
import {LogOutOutline} from "@vicons/ionicons5";
import {NButton, NIcon, NSpin} from "naive-ui";
import {useStore} from "vuex";
import {ref} from "vue";

export default {
  name: "UserInfo",
  components: {
    NIcon, NButton, LogOutOutline, NSpin
  },
  emits: ['send-msg',],
  props: ['userInfo', 'words'],
  setup(props, {emit}) {
    const store = useStore()
    const loadingFlag = ref(false)

    return {
      loadingFlag,
      logout() {
        loadingFlag.value = true
        axios.get('http://127.0.0.1:6498/user/logout').then((res) => {
          if (res.data?.success) {
            emit('send-msg', 'msg' in res.data ? res.data.msg : '退出成功！', 'success')
            store.dispatch('logout')
          } else {
            emit('send-msg', '未知错误，退出失败', 'error')
          }
          loadingFlag.value = false
        }).catch((err) => {
          emit('send-msg', 'msg' in err.response.data?.detail ? err.response.data.detail.msg : '未知错误，退出失败', 'error')
          loadingFlag.value = false
        })
      }
    }
  }
}
</script>

<style scoped>
.user-info > div {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.user-info > div > div:nth-child(1) {
  font-weight: bold;
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
