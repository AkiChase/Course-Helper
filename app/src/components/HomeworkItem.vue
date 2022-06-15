<template>
  <div class="homework-item">
    <div class="homework-title">
      <div :title="`作业ID: ${homework['hw_id']}`" class="enter" @click="toHomeworkDetail(homework['hw_id'])">
        <n-button circle="" size="small">
          <template #icon>
            <n-icon>
              <arrow-forward-outline/>
            </n-icon>
          </template>
        </n-button>
      </div>
      <n-ellipsis style="font-size: 18px;max-width: 45vw">
        {{ homework.title }}
      </n-ellipsis>
    </div>

    <n-space item-style="height: 20px" justify="center">
      <n-tooltip v-if="homework['committable']" trigger="hover">
        <template #trigger>
          <n-icon color="#4daf7c">
            <paper-plane-outline/>
          </n-icon>
        </template>
        作业可提交
      </n-tooltip>
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-icon color="#666">
            <person-circle-outline/>
          </n-icon>
        </template>
        发布人: {{ homework['publisher'] }}
      </n-tooltip>
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-icon color="#f38181">
            <calendar-outline/>
          </n-icon>
        </template>
        截止日期: {{ homework['end_date'] }}
      </n-tooltip>
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-icon :color="homework['score'].length? '#cb8347':''">
            <ribbon-outline/>
          </n-icon>
        </template>
        {{ homework['score'].length ? homework['score'] : '暂无成绩' }}
      </n-tooltip>
    </n-space>
  </div>
</template>

<script>
import {NButton, NEllipsis, NIcon, NSpace, NTooltip} from "naive-ui";
import {
  ArrowForwardOutline,
  CalendarOutline,
  PaperPlaneOutline,
  PersonCircleOutline,
  RibbonOutline
} from "@vicons/ionicons5";
import {useStore} from "vuex";

export default {
  name: "HomeworkItem",
  components: {
    NEllipsis, NSpace, NIcon, NTooltip, NButton,
    PersonCircleOutline, CalendarOutline, RibbonOutline, PaperPlaneOutline, ArrowForwardOutline
  },
  props: ['homework', 'courseName', 'courseId'],
  setup({homework, courseName, courseId}) {
    const store = useStore()
    return {
      async toHomeworkDetail(hwId) {
        await store.dispatch('addHomeworkTabs', {
          ...homework,
          courseName,
          courseId
        })
        await window.$routerPush({name: 'homeworkDetails', params: {activeId: hwId}})
      }
    }
  }
}
</script>

<style scoped>
.homework-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 5px 10px;
  margin: 5px 0;
  font-size: 20px;
  cursor: pointer;
}

.homework-item:hover {
  background-color: #eee;
}

.homework-title {
  display: flex;
  flex-direction: row;
  align-items: start;
  width: 75%;
}

.enter {
  width: 45px;
  height: 100%;
  display: flex;
  justify-content: left;
  align-items: center;
}

.enter:hover {
  color: red;
}


</style>
