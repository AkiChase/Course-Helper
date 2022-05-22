<template>
  <n-spin class="after-login" :show="loadingFlag">
    <n-button @click="logout" class="logout" size="large" circle="">
      <template #icon>
        <n-icon>
          <log-out-outline/>
        </n-icon>
      </template>
    </n-button>
    <div class="user-info">
      <n-tooltip trigger="hover" :show-arrow="false">
        <template #trigger>
          <n-h2 prefix="bar">
            <n-text>
              {{ userInfo.name }}
            </n-text>
          </n-h2>
        </template>
        {{ userInfo.id }}
      </n-tooltip>
      <div>{{ userInfo.college }}</div>
    </div>
    <div class="words">
        <span v-for="p in words">
          {{ p }}
        </span>
    </div>
  </n-spin>
</template>

<script>
import {LogOutOutline} from "@vicons/ionicons5";
import {NButton, NH2, NIcon, NSpin, NText, NTooltip, useMessage} from "naive-ui";
import {useStore} from "vuex";
import {ref} from "vue";
import api from "@/utils/api";
import common from "@/utils/common";

export default {
  name: "UserInfo",
  components: {
    NIcon, NButton, LogOutOutline, NSpin, NH2, NText, NTooltip
  },
  props: ['userInfo', 'words'],
  setup() {
    const store = useStore()
    const loadingFlag = ref(false)
    const message = useMessage()

    return {
      loadingFlag,
      logout() {
        common.showLoading(loadingFlag)
        api.get('http://127.0.0.1:6498/user/logout').then(res => {
          common.sendMsg(message, res.msg, 'success')
          store.dispatch('logout')
          common.hideLoading(loadingFlag)
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          common.hideLoading(loadingFlag)
        })
      }
    }
  }
}
</script>

<style scoped>
.user-info {
  display: flex;
  flex-direction: column;
  align-items: start;
}

.user-info > div {
  color: #aaa;
  font-size: 16px;
  padding-left: 15px;
  position: relative;
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
