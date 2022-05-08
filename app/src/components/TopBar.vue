<template>
  <div :style="`background-color: ${theme.bodyColor}`">
    <div id="drag-block"/>
    <n-button-group>
      <n-button @click="winMinimize()" type="default">
        <template #icon>
          <n-icon>
            <window-minimize-regular/>
          </n-icon>
        </template>
      </n-button>
      <n-button @click="winMaximize()">
        <template #icon>
          <n-icon>
            <window-maximize-regular/>
          </n-icon>
        </template>
      </n-button>
      <n-button @click="winClose()" type="error">
        <template #icon>
          <n-icon>
            <close/>
          </n-icon>
        </template>
      </n-button>
    </n-button-group>
  </div>
</template>

<script>
import {Close} from '@vicons/ionicons5'
import {WindowMinimizeRegular, WindowMaximizeRegular} from '@vicons/fa'
import {NButton, NIcon, NButtonGroup, useThemeVars,} from "naive-ui";

export default {
  name: "TopBar",
  components: {
    Close, WindowMinimizeRegular, WindowMaximizeRegular,
    NIcon, NButton, NButtonGroup
  },
  setup() {
    function winMinimize() {
      window.$electron.win.minimize()
    }

    function winMaximize() {
      window.$electron.win.maximize()
    }

    function winClose() {
      window.$electron.win.close()
    }


    const theme = useThemeVars()

    return {
      winMinimize,
      winMaximize,
      winClose,
      theme
    }
  }
}
</script>

<style scoped>
#drag-block {
  -webkit-app-region: drag;
  flex-grow: 1;
}

.n-button-group {
  margin: 0;
}
</style>
