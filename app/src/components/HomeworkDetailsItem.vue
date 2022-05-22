<template>
  <div class="main">
    <n-h2 prefix="bar">{{ data.courseName }}</n-h2>
    <div class="header">
      <n-h3 style="text-indent:25px">{{ data.title }}</n-h3>

      <n-descriptions :column="2" label-placement="left" size="small" label-style="font-weight: bolder"
                      label-align="center" style="margin-left: 10%">
        <n-descriptions-item label="作业ID">
          <div>{{ hwId }}</div>
        </n-descriptions-item>
        <n-descriptions-item label="发布者">
          <div>{{ data['publisher'] }}</div>
        </n-descriptions-item>
        <n-descriptions-item label="截止日期">
          <div>{{ data['end_date'] }}</div>
        </n-descriptions-item>
        <n-descriptions-item label="分数">
          <div>{{ data.score }}</div>
        </n-descriptions-item>
        <n-descriptions-item label="提交状态">
          {{ data['committable'] ? '待提交' : '不可提交' }}
        </n-descriptions-item>
      </n-descriptions>

    </div>
    <div class="btn">
      <n-button @click="getHomeworkDetail" circle="">
        <template #icon>
          <n-icon>
            <Refresh/>
          </n-icon>
        </template>
      </n-button>
    </div>
    <div :id="`hw${hwId}`" class="main-content scrollbar">
      <n-card :bordered="false" embedded="" v-for="(type, index) in types" :title="typeName[index]">
        <n-empty v-if="emptyFlag[type]" description="空空如也"/>
        <div v-show="!emptyFlag[type]" :class="type"></div>
      </n-card>
    </div>
  </div>
</template>

<script>

import {
  NButton,
  NCard,
  NDescriptions,
  NDescriptionsItem,
  NEllipsis,
  NEmpty,
  NH2,
  NH3,
  NIcon,
  useMessage
} from "naive-ui";
import {onMounted, ref} from "vue";
import api from "@/utils/api";
import common from "@/utils/common";
import {Refresh} from "@vicons/ionicons5";

export default {
  name: "HomeworkDetailsItem",
  components: {
    NButton, NIcon, NCard, NEmpty, NEllipsis, NH2, NH3, NDescriptions, NDescriptionsItem,
    Refresh
  },
  props: ['data'],
  emits: ['download-modal', 'show-hide-loading'],
  setup(prop, context) {
    const message = useMessage()
    const id = prop.data['hw_id']
    const emptyFlag = ref({
      content: true,
      answer: true,
      result: true,
      comment: true
    })
    const types = ['content', 'answer', 'result', 'comment']
    const typeName = ['作业内容', '我的回答', '批改结果', '批改评语']

    function getHomeworkDetail() {
      context.emit('show-hide-loading', true)
      api.get(`http://127.0.0.1:6498/course/getHomeworkDetails/${id}`).then(res => {
        types.forEach(type => {
          const selector = `#hw${id} .${type}`
          document.querySelector(selector).innerHTML = res.data.content[type]
          emptyFlag.value[type] = !res.data.content[type]
        })
        const elements = document.querySelectorAll("a[fid]")
        elements.forEach(element => {
          element.onclick = async (e) => {
            const fId = e.target.getAttribute('fid')
            context.emit('download-modal', fId)
          }
        })
        context.emit('show-hide-loading', false)
      }).catch(err => {
        console.log(err)
        common.sendMsg(message, err, 'error')
        context.emit('show-hide-loading', false)
      })
    }

    onMounted(() => {
      getHomeworkDetail()
    })

    return {
      getHomeworkDetail,
      emptyFlag,
      types, typeName,
      hwId: id,
    }
  }
}
</script>

<style scoped>
.main {
  height: 80%;
  overflow: scroll;
  width: 100%;
  padding: 25px;
  border: 1px #eee solid;
  border-radius: 15px;
  position: relative;
}

.header {
  display: flex;
  flex-direction: column;
}

.btn {
  position: absolute;
  right: 15px;
  top: 15px;
}

.n-card {
  margin: 25px 0;
  border-radius: 15px;
}

</style>
