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


      <n-h2 style="text-align: center;margin: 10px">课程介绍</n-h2>
      <div class="scrollbar" id="course-intro">
        <h4 style="text-align: center">请从课程列表进入课程详情</h4>
      </div>
    </n-spin>
  </div>
</template>

<script>
import {NButton, NH1, NH2, NIcon, NSpin, useMessage} from "naive-ui";
import api from "@/utils/api";
import {onActivated, ref} from "vue";
import "@/style/scrollbar.css";
import {Refresh} from "@vicons/ionicons5";
import {useRoute} from "vue-router";
import common from "@/utils/common";


export default {
  name: "Course",
  components: {
    NButton, NH2, NH1, NSpin, NIcon,
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

#course-intro {
  padding: 10px 25px;
  height: 25%;
  border: 2px #aaa solid;
  overflow-y: scroll;
  border-radius: 15px 5px 5px 15px;
}
</style>
