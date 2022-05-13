<template>
  <div class="main">
    <n-spin class="spin-height" :show="loadingFlag">
      <n-h1 prefix="bar">
        <n-text>{{ courseName }}</n-text>
        <n-button @click="refresh" style="margin-left: 15px" circle="" size="large">
          <template #icon>
            <n-icon>
              <refresh/>
            </n-icon>
          </template>
        </n-button>
      </n-h1>

      <n-card>
        <n-tabs type="line" animated="" pane-class="scrollbar">
          <n-tab-pane display-directive="show" name="课程介绍" tab="课程介绍">
            <n-skeleton v-if="loadingFlag" text="" :repeat="25"/>
            <div v-show="!loadingFlag" id="course-intro">
              <div class="prompt">
                请从课程列表进入课程详情
              </div>
            </div>
          </n-tab-pane>
          <n-tab-pane display-directive="show" name="课程作业" tab="课程作业">
            <n-skeleton v-if="loadingFlag" text="" :repeat="25"/>
            <div v-show="!loadingFlag" id="course-homework">
              <div class="prompt">
                请从课程列表进入课程详情
              </div>
            </div>
          </n-tab-pane>
          <n-tab-pane display-directive="show" name="课程资源" tab="课程资源">
            <n-skeleton v-if="loadingFlag" text="" :repeat="25"/>
            <div v-show="!loadingFlag" id="course-resource">
              <div class="prompt">
                请从课程列表进入课程详情
              </div>
            </div>
          </n-tab-pane>
        </n-tabs>
      </n-card>

      <!--      <n-card size="small" class="scrollbar" title="课程作业" hoverable="" :segmented="{content: true}">-->
      <!--        <n-skeleton v-if="loadingFlag" text="" :repeat="6"/>-->
      <!--        <div v-show="!loadingFlag" id="course-homework">-->
      <!--          <div style="font-size: 25px;color: #aaa;text-align: center;margin-top: 50px">-->
      <!--            请从课程列表进入课程详情-->
      <!--          </div>-->
      <!--        </div>-->
      <!--      </n-card>-->


    </n-spin>
  </div>
</template>

<script>
import {NButton, NCard, NH1, NIcon, NSkeleton, NSpin, NTabPane, NTabs, useMessage} from "naive-ui";
import api from "@/utils/api";
import {onActivated, ref} from "vue";
import "@/style/scrollbar.css";
import {Refresh} from "@vicons/ionicons5";
import {useRoute} from "vue-router";
import common from "@/utils/common";


export default {
  name: "Course",
  components: {
    NButton, NH1, NSpin, NIcon, NSkeleton, NCard, NTabs, NTabPane,
    Refresh,
  },
  props: ['id'],
  setup() {
    const message = useMessage()
    const loadingFlag = ref(false)
    const route = useRoute()
    const courseId = ref('')
    const courseName = ref('无课程')
    const courseIntro = ref('请从课程列表进入课程详情')

    async function getCourseIntro(courseId) {
      common.showLoading(loadingFlag)
      api.get(`http://127.0.0.1:6498/course/getCourseIntroduction/${courseId}`).then(res => {
        document.querySelector('#course-intro').innerHTML = res.data.content
        common.hideLoading(loadingFlag)
      }).catch(err => {
        common.sendMsg(message, err, 'error')
        common.hideLoading(loadingFlag)
      })
    }

    onActivated(() => {
      if ('id' in route.params) {
        const id = route.params.id
        if (courseId.value !== id) {
          courseId.value = id
          courseName.value = route.params.name
          getCourseIntro(id)
        }
      }
    })


    return {
      loadingFlag,
      courseIntro,
      courseName,
      refresh() {
        getCourseIntro(courseId.value)
      },
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
}

.n-tab-pane > div {
  padding: 15px 5%;
}

.prompt {
  font-size: 25px;
  color: #aaa;
  text-align: center;
  margin-top: 50px;
}
</style>
