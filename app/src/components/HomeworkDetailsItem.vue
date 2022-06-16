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
          {{ data['committable'] ? '可提交' : '不可提交' }}
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
    <div :id="`hw${hwId}`" class="scrollbar">
      <n-card :bordered="false" embedded="" v-for="(type, index) in types" :id="type" :key="type"
              :title="typeName[index]">
        <!--内容框-->
        <div v-show="!emptyFlag[type]" :class="type"></div>
        <template v-if="type==='answer'&&data['committable']">
          <n-divider>作业编辑框</n-divider>
          <WangEditor ref="editorRef"/>
          <div style="padding: 25px;text-align: center">
            <n-button size="large" @click="editorSubmit">
              <template #icon>
                <n-icon>
                  <checkmark-circle-sharp/>
                </n-icon>
              </template>
              提交
            </n-button>
          </div>
        </template>
        <n-empty v-else-if="emptyFlag[type]" description="空空如也"/>
      </n-card>
    </div>
  </div>
</template>

<script>

import {
  NButton,
  NCard,
  NDescriptions,
  NDescriptionsItem, NDivider,
  NEllipsis,
  NEmpty,
  NH2,
  NH3,
  NIcon, useDialog,
  useMessage
} from "naive-ui";
import {onMounted, ref, toRefs} from "vue";
import api from "@/utils/api";
import common from "@/utils/common";
import {CheckmarkCircleSharp, Refresh} from "@vicons/ionicons5";
import WangEditor from "@/components/WangEditor";
import {useStore} from "vuex";

export default {
  name: "HomeworkDetailsItem",
  components: {
    NButton, NIcon, NCard, NEmpty, NEllipsis, NH2, NH3, NDescriptions, NDescriptionsItem, NDivider,
    Refresh, CheckmarkCircleSharp,
    WangEditor
  },
  props: ['data'],
  emits: ['download-modal', 'show-hide-loading'],
  setup(props, context) {
    const message = useMessage()
    const dialog = useDialog()
    const store = useStore()
    const editorRef = ref(null)

    const {data} = toRefs(props)
    const id = data.value['hw_id']
    const courseId = data.value.courseId
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

        const answer = res.data.content['answer']

        // 更新可提交状态
        api.get('http://127.0.0.1:6498/course/getHomeworkCommittableState', {
          course_id: courseId,
          hw_id: id
        }).then(res2 => {
          const committable = res2.data['committable']
          store.dispatch('updateHomeworkTabs', {
            hwId: id, data: {'committable': committable}
          })
          if (committable)
            editorRef.value[0].loadCustomHtml(answer) //编辑框载入更新后的作业内容
          context.emit('show-hide-loading', false)
          common.sendMsg(message, res.msg, 'success')
        }).catch()
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
      editorRef,
      editorSubmit() {
        dialog.info({
          title: '提示',
          content: '默认情况下作业不可重复提交，确定提交该作业？',
          positiveText: '确定',
          negativeText: '取消',
          onPositiveClick: () => {
            context.emit('show-hide-loading', true)
            api.post('http://127.0.0.1:6498/course/submitHomework', {
              hw_id: id,
              content: editorRef.value[0].getCustomHtml()
            }).then(res => {
              common.sendMsg(message, res.msg, 'success')
              //刷新作业详情
              getHomeworkDetail()
            }).catch(err => {
              context.emit('show-hide-loading', false)
              common.sendMsg(message, err, 'error')
            })
          }
        })
      },
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

.answer {
  border: 2px #666 solid;
  background-color: white;
  padding: 15px;
  border-radius: 15px;
}

.n-card {
  margin: 25px 0;
  border-radius: 15px;
}

</style>
