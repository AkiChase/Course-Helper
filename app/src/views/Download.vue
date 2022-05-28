<template>
  <div class="main">
    <n-h1 prefix="bar">
      <n-text>下载管理</n-text>
    </n-h1>
    <n-card>
      <n-tabs
          justify-content="space-evenly"
          tab-style="user-select: none"
          type="line">
        <n-tab-pane name="downloadQueue" tab="下载中">
          <div v-if="downloadQueue.length" class="list no-select">
            <DownloadQueueItem v-for="item in downloadQueue" :item="item" :key="item.downloadId"/>
          </div>
          <n-empty style="margin-top: 15%" v-else size="large" description="下载队列空荡荡"/>
        </n-tab-pane>
        <n-tab-pane name="downloadRecords" tab="已完成">
          <template v-if="downloadRecords.length">
            <n-tooltip trigger="hover">
              <template #trigger>
                <n-button style="position: absolute; right: 10px" @click="clearRecords" circle="">
                  <template #icon>
                    <n-icon>
                      <trash-outline/>
                    </n-icon>
                  </template>
                </n-button>
              </template>
              清空下载记录
            </n-tooltip>
            <div class="list no-select">
              <DownloadRecordsItem v-for="item in downloadRecords" :item="item" :key="item.downloadId"/>
            </div>
          </template>
          <n-empty style="margin-top: 15%" v-else size="large" description="下载记录空荡荡"/>
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script>
import {NButton, NCard, NEmpty, NH1, NIcon, NTabPane, NTabs, NText, NTooltip, useDialog, useMessage} from "naive-ui";
import {useStore} from "vuex";
import {computed} from "vue";
import DownloadQueueItem from "@/components/DownloadQueueItem";
import DownloadRecordsItem from "@/components/DownloadRecordsItem";
import {TrashOutline} from "@vicons/ionicons5";
import common from "@/utils/common";


export default {
  name: "Download",
  components: {
    NTabs, NTabPane, NCard, NH1, NText, NButton, NTooltip, NIcon, NEmpty,
    TrashOutline,
    DownloadQueueItem, DownloadRecordsItem
  },
  setup() {
    const store = useStore()
    const message = useMessage()
    const dialog = useDialog()
    const extToIcon = {}

    async function addExtIcon(ext) {
      if (ext in extToIcon) return
      extToIcon[ext] = await window.$electron.utils.app.getFileIcon(`.${ext}`)
    }

    const downloadQueue = computed(() => {
      const queue = store.state.downloadQueue
      queue.forEach(async (item) => {
        const ext = item.fileExt
        await addExtIcon(ext)
        item.fileImg = extToIcon[ext]
      })
      return queue
    })

    const downloadRecords = computed(() => {
      const records = store.state.downloadRecords
      records.forEach(async (item) => {
        if (!window.$electron.utils.fExists(item.filePath)) item.state = 'removed'

        if (item.fileExt !== 'exe') {
          const ext = item.fileExt
          await addExtIcon(ext)
          item.fileImg = extToIcon[ext]
        } else {
          const filePath = item.filePath
          item.fileImg = await window.$electron.utils.app.getFileIcon(filePath)
        }
      })
      return records
    })

    return {
      downloadQueue,
      downloadRecords,
      clearRecords() {
        dialog.warning({
          title: '警告',
          content: '确定清空下载记录？',
          positiveText: '确定',
          negativeText: '取消',
          onPositiveClick: () => {
            store.dispatch('removeDownloadRecord', {})
            common.sendMsg(message, '下载记录已清空', 'success')
          }
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
}

.n-tab-pane {
  height: 65vh;
  overflow-y: scroll !important;
}

.list {
  border: 1px #eee solid;
  margin: 25px;
  border-radius: 15px;
  min-height: 90%;
}

.list > div:last-child {
  border: none;
  border-radius: 0 0 15px 15px;
}

.list > div:first-child {
  border-radius: 15px 15px 0 0;
}

</style>
