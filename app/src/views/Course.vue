<template>
  <div class="main">
    <n-spin class="spin-height" :show="loadingFlag">
      <n-h1 prefix="bar">
        <n-text>{{ courseName }}</n-text>
      </n-h1>

      <n-card>
        <n-tabs v-model:value="activeTabName" type="line" animated=""
                pane-class="scrollbar" justify-content="space-evenly">
          <n-tab-pane display-directive="show" :name="1" tab="课程介绍">
            <n-skeleton v-if="loadingFlag" text="" :repeat="25"/>
            <div v-show="!loadingFlag" id="course-intro">
              <n-empty style="margin-top: 15%" size="huge" description="请从课程列表进入课程详情"/>
            </div>
          </n-tab-pane>
          <n-tab-pane display-directive="show" :name="2" tab="课程作业">
            <n-skeleton v-if="loadingFlag" text="" :repeat="25"/>
            <div v-show="!loadingFlag">
              <div v-if="courseHomework.length">
                <HomeworkItem v-for="(item, index) in courseHomework" :homework="item" :no="index+1"/>
              </div>
              <n-empty style="margin-top: 15%" v-else size="huge" description="暂无作业信息"/>
            </div>
          </n-tab-pane>
          <n-tab-pane display-directive="show" :name="3" tab="课程资源">
            <n-skeleton v-if="loadingFlag" text="" :repeat="25"/>
            <CourseResourcePane ref="refChild" v-show="!loadingFlag" :data="courseResource" :courseId="courseId"/>
          </n-tab-pane>
          <template #suffix>
            <n-button @click="refresh()" circle="" size="small">
              <template #icon>
                <n-icon>
                  <Refresh/>
                </n-icon>
              </template>
            </n-button>
          </template>
        </n-tabs>
      </n-card>
    </n-spin>
  </div>
</template>

<script>
import {
  NButton,
  NCard,
  NEmpty,
  NH1,
  NIcon,
  NSkeleton,
  NSpin,
  NTabPane,
  NTabs,
  useLoadingBar,
  useMessage
} from "naive-ui";
import api from "@/utils/api";
import {onActivated, ref} from "vue";
import "@/style/scrollbar.css";
import {Refresh} from "@vicons/ionicons5";
import {useRoute} from "vue-router";
import common from "@/utils/common";
import HomeworkItem from "@/components/HomeworkItem";
import CourseResourcePane from "@/components/CourseResourcePane";

export default {
  name: "Course",
  components: {
    NButton, NH1, NSpin, NIcon, NSkeleton, NCard, NTabs, NTabPane, NEmpty,
    Refresh,
    HomeworkItem, CourseResourcePane,
  },
  props: ['id'],
  setup() {
    const message = useMessage()
    const loadingBar = useLoadingBar()

    const loadingFlag = ref(false)
    const route = useRoute()
    const courseId = ref('')
    const courseName = ref('无课程')
    const courseIntro = ref('请从课程列表进入课程详情')
    const courseHomework = ref([])
    const courseResource = ref([])
    const activeTabName = ref(1)

    const refChild = ref() // 用于调用课程资源面板组件的内容


    function getCourseIntro(courseId) {
      return new Promise(resolve => {
        api.get(`http://127.0.0.1:6498/course/getCourseIntroduction/${courseId}`).then(res => {
          document.querySelector('#course-intro').innerHTML = res.data.content
          resolve()
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          resolve()
        })
      })
    }

    function getCourseHomework(courseId) {
      return new Promise(resolve => {
        api.get(`http://127.0.0.1:6498/course/getCourseHomework/${courseId}`).then(res => {
          courseHomework.value = res.data['homeworks']
          resolve()
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          resolve()
        })
      })
    }

    function getCourseResource(courseId) {
      return refChild.value.preLoad(courseId)
    }


    function refresh(id = null, tabIndex = null) {
      id = id ?? courseId.value
      if (!id.length) return
      loadingBar.start()
      const proList = []
      switch (tabIndex) {
        case 1:
          proList.push(getCourseIntro(id))
          break
        case 2:
          proList.push(getCourseHomework(id))
          break
        case 3:
          proList.push(getCourseResource(id))
          break
        default:
          proList.push(getCourseIntro(id), getCourseHomework(id), getCourseResource(id))
      }
      return Promise.all(proList).then(() => loadingBar.finish()).catch(() => loadingBar.finish())
    }

    onActivated(() => {
      if ('id' in route.params) {
        const id = route.params.id
        if (courseId.value !== id) {
          common.showLoading(loadingFlag)
          activeTabName.value = 1
          courseId.value = id
          courseName.value = route.params.name
          refresh(id).then(() => common.hideLoading(loadingFlag))
        }
      }
    })

    return {
      courseId,
      loadingFlag,
      courseIntro,
      courseName,
      courseHomework,
      courseResource,
      activeTabName,
      refChild,
      refresh,
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

.n-tab-pane > div {
  padding: 15px 5%;
}
</style>
