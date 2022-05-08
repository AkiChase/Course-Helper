<template>
  <n-config-provider abstract="" :theme="theme">
    <div class="container">
      <TopBar class="top-bar"/>
      <NavigationBar class="nav-bar"/>
      <router-view/>
    </div>
  </n-config-provider>

</template>

<script>
import TopBar from "@/components/TopBar";
import NavigationBar from "@/components/NavigationBar";
import {NGrid, NGi, darkTheme, NConfigProvider} from "naive-ui";
import {computed, onMounted} from "vue";
import {useStore} from "vuex";

export default {
  name: "Header",
  components: {
    NavigationBar,
    TopBar,
    NGrid, NGi, NConfigProvider
  },
  setup() {
    const store = useStore()

    onMounted(() => {
      window.$ws.connect()
    })

    const theme = computed(() => store.state.themeValue === 'darkTheme' ? darkTheme : null)

    return {
      theme
    }
  }
}
</script>


<style scoped>
.container {
  display: grid;
  height: 100%;
  width: 100%;
  grid-template-rows: auto 1fr;
  grid-template-columns: 75px 1fr;
}

.top-bar {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.nav-bar {
  grid-row-start: 1;
  grid-row-end: 3;
}

</style>
