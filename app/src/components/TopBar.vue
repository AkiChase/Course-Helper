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
import {useStore} from "vuex";

export default {
  name: "TopBar",
  components: {
    Close, WindowMinimizeRegular, WindowMaximizeRegular,
    NIcon, NButton, NButtonGroup
  },
  setup() {
    const store = useStore()

    return {
      winMinimize() {
        window.$electron.win.minimize()
      },
      winMaximize() {
        window.$electron.win.maximize()
      },
      winClose() {
        window.$electron.store.set('downloadRecords', JSON.parse(JSON.stringify((store.state.downloadRecords))))
        window.$electron.win.close()
      }
    }
  }
}
</script>

<style scoped>
.main {
  border-top-right-radius: 15px;
}

#drag-block {
  -webkit-app-region: drag;
  flex-grow: 1;
}

.n-button-group {
  margin: 0;
}

.close {
  border-top-right-radius: 15px;
}

.close:hover {
  border-top-right-radius: 15px;
  background-color: #c12c1f;
  color: #fff;
}

.close:active {
  border-top-right-radius: 15px;
  background-color: #ff3a29;
  color: #fff;
}
</style>
