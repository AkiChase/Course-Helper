<template>
  <div class="container">
    <TopBar/>
    <NavigationBar/>
    <router-view/>
  </div>
</template>

<script>
import TopBar from "@/components/TopBar";
import NavigationBar from "@/components/NavigationBar";
import {NGrid, NGi} from "naive-ui";
import {onMounted} from "vue";
// import {onMounted} from "vue";

export default {
  name: "Header",
  components: {
    NavigationBar,
    TopBar,
    NGrid, NGi
  },
  setup() {
    onMounted(() => {
      window.$ws.connect()
    })
  }
}
</script>


<style scoped>
.container {
  display: grid;
  height: 100%;
  width: 100%;
  grid-template-rows: auto 1fr;
  grid-template-columns: 100px 1fr;
}
</style>
