<template>
  <div class="main">
    <n-spin class="spin-height" :show="loadingFlag">
      <n-h1 prefix="bar">
        <n-text>课程列表</n-text>
        <n-button @click="getCourseList" style="margin-left: 15px" circle="" size="large">
          <template #icon>
            <n-icon>
              <refresh/>
            </n-icon>
          </template>
        </n-button>
      </n-h1>

      <div class="course-container">
        <n-empty v-if="!courseList.length" size="huge" description="课程列表空空如也"></n-empty>
        <n-grid v-else class="course-list" :x-gap="15" :y-gap="15" cols="2 900:3 1200:4">
          <n-grid-item v-for="(item, index) in courseList">
            <CourseItem :num="index+1" :info="item"/>
          </n-grid-item>
        </n-grid>
      </div>
    </n-spin>
  </div>
</template>

<script>
import {onMounted, ref, watch} from "vue";
import {NButton, NEmpty, NGrid, NGridItem, NH1, NIcon, NSpin, NText, useMessage} from "naive-ui";
import {Refresh} from "@vicons/ionicons5";
import CourseItem from "@/components/CourseItem";
import {useStore} from "vuex";
import api from "@/utils/api";

export default {
  name: "Home",
  components: {
    NIcon, NButton, NGrid, NGridItem, NH1, NText, NSpin, NEmpty,
    Refresh,
    CourseItem
  },
  setup() {
    const store = useStore()
    const message = useMessage()

    const courseList = ref([])
    const loadingFlag = ref(false)

    function sendMsg(msg, type = 'default', duration = 2500, otherOptions = {}) {
      message.create(msg, {
        type,
        duration,
        closable: true,
        keepAliveOnHover: true,
        ...otherOptions
      })
    }

    function getCourseList() {
      if (!store.state.loginState) {
        sendMsg('请先登录！', 'error')
        return
      }

      loadingFlag.value = true
      api.get('http://127.0.0.1:6498/course/getCourseList').then(res => {
        courseList.value = res.data
        loadingFlag.value = false
      }).catch(e => {
        sendMsg(e, 'error')
        loadingFlag.value = false
      })
    }

    watch(
        () => store.state.loginState,
        (newState, preState) => {
          if (newState === false && preState === true) {
            console.log('登出了')
            courseList.value = []
          } else {
            console.log('登录了')
            getCourseList()
          }
        }
    )

    onMounted(() => getCourseList())

    return {
      courseList,
      loadingFlag,
      getCourseList,
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
  /*background-color: rgba(255, 255, 255, 0.8);*/
}

.course-container {
  background-color: rgba(255, 255, 255, 0.8);
  min-height: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 25px;
  padding: 25px;
}

</style>

<style>
.spin-height,
.spin-height > * {
  height: 100%;
}
</style>
