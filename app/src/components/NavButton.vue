<template>
  <router-link custom v-slot="{ navigate, isExactActive }" :to="to">
    <div @click="navigate" :class="isExactActive ? 'router-link router-link-exact-active' : 'router-link'">
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
}

.router-link:not(.router-link-exact-active):hover {
  background-color: #65bb8e;
  /*color: #E9EFC0;*/
  transition: background-color 0.5s, color 0.5s;
}


.router-link-exact-active {
  background-color: #409368;
  transition: background-color 0.5s, color 0.5s;
  /*color: #E9EFC0;*/
}

</style>
