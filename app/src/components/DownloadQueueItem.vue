<template>
  <div class="main">
    <div class="img-box">
      <img :src="item.fileImg" :alt="item.fileName">
    </div>
    <div class="content">
      <n-ellipsis
          :style="`max-width: 60vw;font-weight: bolder;font-size: larger;${item.state==='removed'?'text-decoration:line-through':''}`">
        {{ item.fileName }}
      </n-ellipsis>

      <!--下载中-->
      <template v-if="item.state==='downloading'">
        <div class="info">
          <div>{{ item.speed }}</div>
          <div>{{ item.downSize }} / {{ item.fileSize }}</div>
          <div>{{ item.timeRemain }}</div>
        </div>
        <n-progress
            status="success"
            :percentage="Math.round(item.downSizeRaw*100 / item.fileSizeRaw)"
            :show-indicator="true"
            :height="10"
            indicator-placement="inside"
            processing=""
        />
      </template>
      <!--等待下载-->
      <div v-else class="info">
        <div>{{ item.fileSize }}</div>
        <div>等待下载</div>
      </div>
    </div>
    <div class="btn-group">
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-icon :size="25">
            <information-circle-outline/>
          </n-icon>
        </template>
        下载ID: {{ item.downloadId }}
      </n-tooltip>
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-icon :size="25">
            <folder-outline/>
          </n-icon>
        </template>
        保存路径: {{ item.filePath }}
      </n-tooltip>
    </div>
  </div>
</template>

<script>
import {NButton, NEllipsis, NIcon, NProgress, NTooltip} from "naive-ui";
import {InformationCircleOutline, FolderOutline} from "@vicons/ionicons5";

export default {
  name: "DownloadQueueItem",
  components: {
    NEllipsis, NProgress, NButton, NTooltip, NIcon,
    InformationCircleOutline, FolderOutline
  },
  props: ['item'],
  setup() {
    return {}
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
</style>
