<template>
  <div class="main">
    <div class="img-box">
      <img class="no-drag" :style="item.state==='removed'?'filter: grayscale(80%);':''" :src="item.fileImg"
           :alt="item.fileName">
    </div>
    <div class="content">
      <n-ellipsis
          :style="`max-width: 60vw;font-weight: bolder;font-size: larger;${item.state==='removed'?'text-decoration:line-through':''}`">
        {{ item.fileName }}
      </n-ellipsis>
      <div class="info">
        <div>{{ item.fileSize }}</div>
        <div :class="item.state">{{ item.state in state ? state[item.state] : '文件状态未知' }}</div>
      </div>
    </div>
    <div class="btn-group">
      <n-icon @click="removeRecord" title="删除记录" :size="22" class="close">
        <close-outline/>
      </n-icon>

      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button circle="">
            <template #icon>
              <n-icon>
                <information-outline/>
              </n-icon>
            </template>
          </n-button>
        </template>
        下载ID: {{ item.downloadId }}
      </n-tooltip>
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button @click="showFileInFolder" circle="">
            <template #icon>
              <n-icon>
                <folder-open-outline/>
              </n-icon>
            </template>
          </n-button>
        </template>
        {{ item.filePath }}
      </n-tooltip>
    </div>
  </div>
</template>

<script>
import {NButton, NEllipsis, NIcon, NTooltip} from "naive-ui";
import {CloseOutline, FolderOpenOutline, InformationOutline} from "@vicons/ionicons5";
import {useStore} from "vuex";


export default {
  name: "DownloadRecordsItem",
  components: {
    NEllipsis, NTooltip, NButton, NIcon,
    FolderOpenOutline, InformationOutline, CloseOutline,
  },
  props: ['item'],
  setup({item}) {
    const store = useStore()
    return {
      state: {
        'finished': '文件已下载',
        'removed': '文件已移除',
        'error': '下载失败'
      },
      showFileInFolder() {
        window.$electron.utils.shell.showItemInFolder(item.filePath)
      },
      removeRecord() {
        store.dispatch('removeDownloadRecord', {downloadId: item.downloadId})
      }
    }
  }
}
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px #eee solid;
  position: relative;
}

.main:hover {
  background-color: #f4fafe;
}

.content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  width: 60%;
  padding: 15px 25px;
}

.content .info {
  display: flex;
  flex-direction: row;
  justify-content: left;
  color: #666;
  margin-top: 5px;
  font-size: small;
}

.content .info > div {
  margin-right: 10%;
}

.content .info .error{
  color: #c12c1f;
}

.img-box {
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.img-box > img {
  width: 40px;
  height: 40px;
}


.btn-group {
  width: 100px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  margin-top: 20px;
}

.btn-group .close {
  position: absolute;
  top: 5px;
  right: 5px;
  color: #666;
  border-radius: 100px;
}

.btn-group .close:hover {
  color: #aaa;
}

</style>
