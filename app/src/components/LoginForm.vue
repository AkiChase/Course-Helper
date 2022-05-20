<template>
  <n-spin :show="loadingFlag">
    <n-form
        ref="formRef"
        label-placement="left"
        label-width="80"
        :model="loginFormVal"
        :rules="loginRules"
        size="large"
    >
      <h2 style="text-align: center">用户登录</h2>
      <n-form-item label="统一账号" path="userId">
        <n-input clearable="" v-model:value="loginFormVal.userId" placeholder="输入统一身份认证账号">
          <template #prefix>
            <n-icon :component="User"/>
          </template>
        </n-input>
      </n-form-item>
      <n-form-item label="统一密码" path="userPw">
        <n-input
            type="password"
            show-password-on="click"
            placeholder="输入统一身份认证密码"
            v-model:value="loginFormVal.userPw"
        >
          <template #prefix>
            <n-icon :component="Key"/>
          </template>
        </n-input>
      </n-form-item>
      <n-form-item label="VPN账号" path="vpnId">
        <n-input v-model:value="loginFormVal.vpnId" placeholder="输入厦大VPN账号">
          <template #prefix>
            <n-icon :component="Planet"/>
          </template>
        </n-input>
      </n-form-item>
      <n-form-item label="VPN密码" path="vpnPw">
        <n-input
            type="password"
            show-password-on="click"
            placeholder="输入厦大VPN密码"
            v-model:value="loginFormVal.vpnPw"
        >
          <template #prefix>
            <n-icon :component="Key"/>
          </template>
        </n-input>
      </n-form-item>
      <div style="text-align: right">
        <n-checkbox v-model:checked="rememberFlag">
          记住账号密码
        </n-checkbox>
      </div>
      <div style="display: flex;justify-content: center;margin-top: 15px">
        <n-button @click="login" size="large" type="success" style="padding: 10px 50px">登 录</n-button>
      </div>
    </n-form>
  </n-spin>
</template>

<script>
import {NButton, NCheckbox, NForm, NFormItem, NIcon, NInput, NSpin, useMessage} from "naive-ui";
import {Key, User} from "@vicons/fa";
import {Planet} from "@vicons/ionicons5";
import {useStore} from "vuex";
import {ref, watch} from "vue";
import api from "@/utils/api";
import common from "@/utils/common";

export default {
  name: "LoginForm",
  components: {
    NButton, NForm, NFormItem, NInput, NIcon, NCheckbox, NSpin,
    User, Key, Planet
  },
  setup() {
    const electronStore = window.$electron.store
    const store = useStore()
    const loadingFlag = ref(false)
    const message = useMessage()

    const formRef = ref(null)

    // 是否记住账号密码
    let rememberFlag = ref(electronStore.get('rememberFlag', false))
    watch(rememberFlag, (newFlag) => {
      electronStore.set('rememberFlag', newFlag)
    })

    const loginFormVal = ref({
      userId: "",
      userPw: "",
      vpnId: "",
      vpnPw: ""
    })
    // 若记住账号密码则填充
    if (rememberFlag) {
      for (const k in loginFormVal.value) {
        loginFormVal.value[k] = electronStore.get(k, '')
      }
    }

    return {
      formRef,
      loginFormVal,
      rememberFlag,
      loadingFlag,
      loginRules: {
        userId: {
          required: true,
          message: "请输入统一身份账号",
          trigger: "blur"
        },
        userPw: {
          required: true,
          message: "请输入统一身份密码",
          trigger: "blur"
        },
        vpnId: {
          required: true,
          message: "请输入VPN账号",
          trigger: "blur"
        },
        vpnPw: {
          required: true,
          message: "请输入VPN密码",
          trigger: "blur"
        },
      },
      User, Key, Planet,
      login() {
        // ?. 若左边非null或 undefined 才继续访问右边
        formRef.value?.validate().then(() => {
          common.showLoading(loadingFlag)
          // 保存最新账号密码 或 清空保存的密码
          electronStore.setWithObj(rememberFlag.value ? {...loginFormVal.value} : {
            userId: "",
            userPw: "",
            vpnId: "",
            vpnPw: ""
          })

          api.post('http://127.0.0.1:6498/user/login', {
            user_id: loginFormVal.value.userId,
            user_pw: loginFormVal.value.userPw,
            vpn_id: loginFormVal.value.vpnId,
            vpn_pw: loginFormVal.value.vpnPw
          }).then(res => {
            common.sendMsg(message, res.msg, 'success')
            store.dispatch('saveLoginInfo', {...res.data})
            common.hideLoading(loadingFlag)
          }).catch(err => {
            common.sendMsg(message, err, 'error')
            common.hideLoading(loadingFlag)
          })
        }).catch(() => {
        })
      },
    }
  }
}
</script>

<style scoped>

</style>
