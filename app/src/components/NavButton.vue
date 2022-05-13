<template>
  <router-link custom v-slot="{ navigate, isActive }" :to="to">
    <div @click="navigate" :class="isActive ? 'router-link router-link-active' : 'router-link'">
      <n-icon :size="30">
        <slot></slot>
      </n-icon>
    </div>
  </router-link>
</template>

<script>
import {NIcon} from "naive-ui";

export default {
  name: "NavButton",
  props: ['to'],
  components: {
    NIcon
  }
}
</script>

<style scoped>

.router-link {
  width: 100%;
  text-align: center;
  padding: 8px 0;
  cursor: pointer;
  color: #fff;
  transition: background-color 0.5s, color 0.5s;
}

.router-link:not(.router-link-active):hover {
  background-color: #65bb8e;
  transition: background-color 0.5s, color 0.5s;
}


.router-link-active {
  background-color: #409368;
  transition: background-color 0.5s, color 0.5s;
}

</style>
