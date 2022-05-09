<template>
  <div class="main">
    <div id="drag-block"/>
    <n-button-group>
      <n-button @click="winMinimize()" :bordered="false" title="最小化">
        <template #icon>
          <n-icon>
            <window-minimize-regular/>
          </n-icon>
        </template>
      </n-button>
      <n-button @click="winMaximize()" :bordered="false" title="最大化">
        <template #icon>
          <n-icon>
            <window-maximize-regular/>
          </n-icon>
        </template>
      </n-button>
      <n-button @click="winClose()" :bordered="false" ghost="" class="close" title="关闭">
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
      winClose,
    }
  }
}
</script>

<style scoped>
.main{
  border-top-right-radius: 15px;
}

#drag-block {
  -webkit-app-region: drag;
  flex-grow: 1;
}

.n-button-group {
  margin: 0;
}

.close{
  border-top-right-radius: 15px;
}

.close:hover {
  border-top-right-radius: 15px;
  background-color: #c12c1f;
  color: #fff;
}

.close:
</style>
