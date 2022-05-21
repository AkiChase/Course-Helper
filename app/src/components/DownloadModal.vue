<template>
  <n-modal v-model:show="showModal" :on-after-leave="cancel">
    <n-card
        style="width: 600px;position: relative"
        :title="data.title"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
    >
      <n-form
          :model="data.form"
          :rules="rules"
          label-placement="left"
      >
        <n-form-item label="目录" path="dirPath">
          <n-input-group>
            <n-input :value="data.form.dirPath" readonly="" placeholder="选择文件位置"/>
            <n-button @click="selectDirPath" type="primary" ghost="">
              选择
            </n-button>
          </n-input-group>
        </n-form-item>
        <n-form-item label="选项">
          <n-space>
            <n-checkbox v-model:checked="data.form.treeFlag">
              <n-tooltip trigger="hover">
                <template #trigger>
                  保留目录结构
                </template>
                按课程资源的树状结构保存文件到下载目录
              </n-tooltip>
            </n-checkbox>
          </n-space>
        </n-form-item>
      </n-form>

      <n-button @click="download" style="position: absolute; right: 25px;bottom: 25px" round="" type="success">
        下载
      </n-button>

    </n-card>
  </n-modal>
</template>

<script>
import {NButton, NCard, NCheckbox, NForm, NFormItem, NInput, NInputGroup, NModal, NSpace, NTooltip} from "naive-ui";
import {ref} from "vue";

export default {
  name: "DownloadModal",
  components: {
    NModal, NCard, NForm, NFormItem, NInput, NInputGroup, NButton, NCheckbox, NTooltip, NSpace,
  },
  props: ['data'],
  setup({data}) {
    const showModal = ref(false)
    let resolveRef = null

    return {
      showModal,
      rules: {
        dirPath: {
          required: true,
          message: "请选择下载保存目录",
          trigger: "blur"
        }
      },
      selectDirPath: async () => {
        const res = await window.$electron.utils.dialog.showOpenDialog({
          title: '请选择下载保存目录',
          defaultPath: data.form.dirPath,
          properties: ['openDirectory']
        })
        if (res?.filePaths?.length) {
          data.form.dirPath = res.filePaths[0]
        }
      },
      cancel() {
        if (resolveRef !== null) {
          resolveRef.reject()
          resolveRef = null
        }
      },
      download() {
        resolveRef.resolve()
        resolveRef = null
        showModal.value = false
      },
      showDownloadModal: async () => {
        showModal.value = true
        return new Promise((resolve, reject) => {
          resolveRef = {resolve, reject}
        })
      },
    }
  }
}
</script>

<style scoped>

</style>
