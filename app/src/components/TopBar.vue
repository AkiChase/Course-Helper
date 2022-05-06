<template>
  <div id="header">
    <div id="drag-block"></div>
    <n-button-group>
      <n-button @click="winMinimize()" type="default">
        <template #icon>
          <n-icon>
            <window-minimize-regular/>
          </n-icon>
        </template>
      </n-button>
      <n-button @click="winMaximize()" type="default">
        <template #icon>
          <n-icon>
            <window-maximize-regular/>
          </n-icon>
        </template>
      </n-button>
      <n-button @click="winClose()" type="default">
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
import {NButton, NIcon, NButtonGroup} from "naive-ui";

export default {
  name: "TopBar",
  components: {
    Close, WindowMinimizeRegular, WindowMaximizeRegular,
    NIcon, NButton, NButtonGroup
  },
  setup() {
    // onMounted(() => {
    //   console.log('TopBar的锚定', process.env)
    // })

    function winMinimize() {
      window.$electron.win.minimize()
    }

    function winMaximize() {
      window.$electron.win.maximize()
    }

    function winClose() {
      window.$electron.win.close()
    }

    return {
      winMinimize,
      winMaximize,
      winClose
    }
  }
}
</script>

<style scoped>
#header {
  grid-column-start: 1;
  grid-column-end: 3;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

#drag-block {
  -webkit-app-region: drag;
  flex-grow: 1;
}

.n-button-group {
  margin: 0;
}
</style>
