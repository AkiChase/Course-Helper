<template>
  <div style="position: relative">
    <n-input style="width: calc(100% - 30px);margin-bottom: 30px" v-model:value="pattern"
             placeholder="搜索 ( 仅搜索已加载的内容 )"/>
    <n-tooltip trigger="hover">
      <template #trigger>
        <n-button @click="loadAll" circle="" style="position: absolute;right: 15px">
          <template #icon>
            <n-icon>
              <bulb-outline/>
            </n-icon>
          </template>
        </n-button>
      </template>
      加载资源树全部分支
    </n-tooltip>
    <n-tree
        :pattern="pattern"
        :data="data"
        :on-load="onLoad"
        :expanded-keys="expandedKeys"
        :checked-keys="checkedKeys"
        @update:checked-keys="handleCheckedKeysChange"
        @update:expanded-keys="handleExpandedKeysChange"

        label-field="res_name"
        block-line=""
        cascade=""
        checkable=""
    />
  </div>
</template>

<script>
import {NButton, NIcon, NInput, NSpace, NTooltip, NTree, useLoadingBar, useMessage} from "naive-ui";
import {h, ref} from "vue";
import api from "@/utils/api";
import common from "@/utils/common";
import {BulbOutline} from "@vicons/ionicons5";
import {Folder, FilePdf, FilePowerpoint, FileWord, FileExcel, FileVideo, FileAlt, FileArchive} from "@vicons/fa";

export default {
  name: "CourseResourcePane",
  components: {
    NInput, NTree, NButton, NSpace, NIcon, NTooltip,
    BulbOutline, Folder, FilePdf, FilePowerpoint, FileWord, FileExcel, FileVideo, FileArchive, FileAlt
  },
  props: ['courseId'],
  setup(props) {
    const data = ref([])
    const message = useMessage()
    const loadingBar = useLoadingBar()

    const expandedKeys = ref([]);
    const checkedKeys = ref([]);

    const nameToIcon = {
      'folder': [Folder, '#f4d16e'],
      'pdf': [FilePdf, '#9e2a22'],
      'powerpoint': [FilePowerpoint, '#e18a3b'],
      'word': [FileWord, '#4994c4'],
      'excel': [FileExcel, '#4c8045'],
      'video': [FileVideo, '#c7c6b6'],
      'zip': [FileArchive, '#ffc757']
    }

    function typeNameToPrefix(name) {
      return name in nameToIcon ? () => h(NIcon, {
        component: nameToIcon[name][0],
        color: nameToIcon[name][1]
      }) : () => h(NIcon, {component: FileAlt, color: '#686a67'})
    }

    function addPrefix(items) {
      items.forEach(item => {
        item.suffix = typeNameToPrefix(item['type_name'])
        if (item?.children?.length) {
          addPrefix(item.children)
        }
      })
    }

    function load(courseId, folderId, deep = false) {
      let url = `http://127.0.0.1:6498/course/getCourseResource/${courseId}?folder_id=${folderId}`
      if (deep) url += '&deep=true'
      return new Promise(resolve => {
        api.get(url).then(res => {
          const resData = res.data['content']
          resData.forEach(item => {
            item.isLeaf = item['type_name'] !== 'folder'
          })
          addPrefix(resData)

          resolve(resData)
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          resolve([])
        })
      })
    }

    return {
      data,
      pattern: ref(""),
      expandedKeys,
      checkedKeys,
      onLoad(node) {
        const folderId = node['folder_id']
        const courseId = props.courseId
        return load(courseId, folderId).then(res => {
          if (res.length) node.children = res
        })
      },
      preLoad(courseId) {
        return load(courseId, 0).then(res => {
          data.value = res
        })
      },
      loadAll() {
        loadingBar.start()
        load(props.courseId, 0, true).then(res => {
          data.value = res
          const expands = []
          res.forEach(item => {
            if (item['type_name'] === 'folder') {
              expands.push(item['key'])
            }
          })
          expandedKeys.value = expands
          loadingBar.finish()

        })
      },
      handleExpandedKeysChange(keys) {
        expandedKeys.value = keys;
      },
      handleCheckedKeysChange(keys) {
        checkedKeys.value = keys;
      },
    }
  }
}
</script>

<style scoped>

</style>
