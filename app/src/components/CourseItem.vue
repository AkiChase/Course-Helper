<template>
  <n-thing class="course">
    <template #avatar>
      <n-space style="height: 100%" align="center">
        <n-button title="进入课程" circle="">
          <template #icon>
            <n-icon>
              <arrow-forward-circle/>
            </n-icon>
          </template>
        </n-button>
      </n-space>
    </template>
    <template #header>
      <n-ellipsis style="max-width: 200px; font-weight: bold;">
        {{ info.name }}
      </n-ellipsis>
    </template>
    <template #header-extra>
      <span class="num"># {{num}}</span>
    </template>
    <template #description>
      <n-ellipsis style="max-width: 200px">
        <span style="font-weight: bold">{{ info.teacher }}</span> - {{ info.college }}
      </n-ellipsis>
    </template>
  </n-thing>

</template>

<script>
import {NAvatar, NButton, NEllipsis, NIcon, NSpace, NThing} from "naive-ui";
import {ArrowForwardCircle, Information} from "@vicons/ionicons5";

export default {
  name: "CourseItem",
  props: ['info', 'num'],
  components: {
    NThing, NAvatar, NIcon, NButton, NSpace, NEllipsis,
    ArrowForwardCircle, Information,
  },
}
</script>

<style scoped>
.course {
  width: 250px;
  padding: 25px;
  margin: auto;
  background-color: white;
  border: 2px #eee solid;
  border-radius: 15px;
  transition: box-shadow 0.5s;
  position: relative;
}

.course:hover {
  box-shadow: #aaa 0 0 10px;
  transition: box-shadow 0.5s;
}

.num {
  position: absolute;
  top: 5px;
  right: 5px;
  color: #aaa;
}
</style>
