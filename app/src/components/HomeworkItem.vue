<template>
  <div class="homework-item">
    <div class="homework-title">
      <div class="serial-num">#{{ no }}</div>
      <n-ellipsis style="font-size: 18px">
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
        截止日期: {{ homework['end_data'] }}
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
import {NEllipsis, NIcon, NSpace, NTooltip} from "naive-ui";
import {PersonCircleOutline, CalendarOutline, RibbonOutline, PaperPlaneOutline} from "@vicons/ionicons5";

export default {
  name: "HomeworkItem",
  components: {
    NEllipsis, NSpace, NIcon, NTooltip,
    PersonCircleOutline, CalendarOutline, RibbonOutline, PaperPlaneOutline,
  },
  props: ['homework', 'no']
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
}

.homework-item:hover {
  background-color: #eee;
}

.homework-title {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 70%;
}

.serial-num {
  font-weight: bolder;
  font-size: 15px;
  color: #aaa;
  width: 45px;
}


</style>
