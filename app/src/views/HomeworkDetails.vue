<template>
  <div class="main">
    <n-spin :show="loadingFlag">
      <n-h1 prefix="bar">
        <n-text>作业详情</n-text>
      </n-h1>
      <n-card>
        <n-tabs v-if="homeworkTabs.length"
                v-model:value="activeTab"
                type="card"
                closable=""
                @close="handleClose"
        >
          <n-tab-pane
              v-for="(data, index) in homeworkTabs"
              :tab="`作业${index+1}`"
              :name="data['hw_id']"
              display-directive="show:lazy"
          >
            <HomeworkDetailsItem @download-modal="downloadFile" @show-hide-loading="showHideLoading" :data="data"/>
          </n-tab-pane>
        </n-tabs>
        <n-empty v-else style="margin-top: 20vh" size="large" description="暂无打开的作业"/>
      </n-card>
    </n-spin>
    <DownloadModal ref="downloadModalRef" :data="downloadModalData"/>
  </div>
</template>

<script>
import {NCard, NEmpty, NH1, NSpin, NTabPane, NTabs, NText, useMessage} from "naive-ui";
import HomeworkDetailsItem from "@/components/HomeworkDetailsItem";
import {computed, onActivated, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {useStore} from "vuex";
import DownloadModal from "@/components/DownloadModal";
import common from "@/utils/common";
import api from "@/utils/api";


export default {
  name: "HomeworkDetails",
  components: {
    NTabs, NSpin, NTabPane, NCard, NH1, NText, NEmpty,
    HomeworkDetailsItem, DownloadModal
  },
  setup() {
    const store = useStore()
    const message = useMessage()
    const route = useRoute()
    const loadingFlag = ref(false)
    const activeTab = ref(null)

    const downloadModalRef = ref(null)
    const downloadModalData = ref({
      title: '新建下载任务',
      form: {
        dirPath: '',
      }
    })


    const homeworkTabs = computed(() => store.state.homeworkTabs)

    onActivated(() => {
      if (route.params?.activeId) {
        activeTab.value = route.params.activeId
      }
    })

    onMounted(async () => {
      let path = await window.$electron.utils.app.getPath('downloads')
      path = window.$electron.utils.mkDir(path, 'Course Helper')
      downloadModalData.value.form.dirPath = path
    })

    function handleClose(hwId) {
      store.dispatch('removeHomeworkTabs', hwId).then(index => {
        if (homeworkTabs.value.length) {
          index = index === homeworkTabs.value.length ? index - 1 : index
          activeTab.value = homeworkTabs.value[index]['hw_id']
        }
      })
    }

    return {
      loadingFlag,
      homeworkTabs,
      activeTab,
      downloadModalData,
      downloadModalRef,
      handleClose,
      showHideLoading(flag) {
        loadingFlag.value = flag
      },
      downloadFile(fId) {
        downloadModalRef.value.showDownloadModal().then(() => {
          const dirPath = downloadModalData.value.form.dirPath

          common.showLoading(loadingFlag)
          api.post('http://127.0.0.1:6498/course/downloadFile', {
            file_id: fId,
            dir_path: dirPath
          }).then(res => {
            common.sendMsg(message, res.msg, 'success')
            common.hideLoading(loadingFlag)
          }).catch(err => {
            common.sendMsg(message, err, 'error')
            common.hideLoading(loadingFlag)
          })
        }).catch(e => {
          console.log(e)
          common.sendMsg(message, '下载取消', 'error')
        })
      }
    }
  }
}
</script>

<style scoped>
.main {
  width: auto;
  min-width: 80%;
  margin: auto;
  height: 100%;
  padding: 0 25px;
}

.n-card {
  border-radius: 25px;
  height: 80vh;
}

.n-tab-pane {
  height: 65vh;
  overflow-y: scroll !important;
}

.n-tab-pane > div {
  padding: 15px 5%;
}

</style>
