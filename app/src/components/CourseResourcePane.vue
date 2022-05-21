<template>
  <div style="position: relative">
    <n-input style="width: calc(100% - 70px);margin-bottom: 30px" v-model:value="pattern"
             placeholder="搜索 ( 仅搜索已加载的内容 )"/>
    <n-tooltip trigger="hover">
      <template #trigger>
        <n-button @click="loadAll" circle="" style="position: absolute;right: 10px">
          <template #icon>
            <n-icon>
              <bulb-outline/>
            </n-icon>
          </template>
        </n-button>
      </template>
      加载资源树全部分支
    </n-tooltip>
    <n-tooltip trigger="hover">
      <template #trigger>
        <n-button @click="downloadSelected" circle="" style="position: absolute;right: 55px">
          <template #icon>
            <n-icon>
              <download-outline/>
            </n-icon>
          </template>
        </n-button>
      </template>
      下载选中项: 已选{{ checkedKeys.length }}项
    </n-tooltip>
    <n-spin :show="loadingFlag">
      <n-tree
          :pattern="pattern"
          :data="data"
          :on-load="onLoad"
          :expanded-keys="expandedKeys"
          :checked-keys="checkedKeys"
          :node-props="treeNodeProps"
          @update:checked-keys="handleCheckedKeysChange"
          @update:expanded-keys="handleExpandedKeysChange"

          check-strategy="child"
          label-field="res_name"
          block-line=""
          cascade=""
          checkable=""
      />
    </n-spin>
    <n-dropdown
        trigger="manual"
        placement="bottom-start"
        :show="showDropdown"
        :options="dropdownOptions"
        :x="posX"
        :y="posY"
        @select="handleSelect"
        @clickoutside="handleClickOutside"
    />
    <n-modal v-model:show="showModal">
      <n-card
          style="width: 600px"
          title="课程资源信息"
          :bordered="false"
          size="huge"
          role="dialog"
          aria-modal="true"
      >
        <n-space vertical="">
          <h3 style="text-align: center">
            <n-ellipsis style="max-width: 500px">
              {{ modelData.fileTitle }}
            </n-ellipsis>
          </h3>
          <n-space justify="space-between">
            <span>文件名:</span>
            <n-ellipsis style="max-width: 450px">
              {{ modelData.fileName }}
            </n-ellipsis>
          </n-space>
          <n-space justify="space-between">
            <span>文件大小:</span>
            <span>{{ modelData.size }}</span>
          </n-space>
        </n-space>

      </n-card>
    </n-modal>
  </div>
</template>

<script>
import {
  NButton,
  NCard,
  NDropdown, NEllipsis,
  NIcon,
  NInput,
  NModal,
  NSpace, NSpin,
  NTooltip,
  NTree,
  useLoadingBar,
  useMessage
} from "naive-ui";
import {h, onMounted, ref} from "vue";
import api from "@/utils/api";
import common from "@/utils/common";
import {BulbOutline, DownloadOutline, InformationCircleOutline} from "@vicons/ionicons5";
import {Folder, FilePdf, FilePowerpoint, FileWord, FileExcel, FileVideo, FileAlt, FileArchive} from "@vicons/fa";
import {useStore} from "vuex";

export default {
  name: "CourseResourcePane",
  components: {
    NInput, NTree, NButton, NSpace, NIcon, NTooltip, NDropdown, NModal, NCard, NSpin, NEllipsis,
    BulbOutline, Folder, FilePdf, FilePowerpoint, FileWord, FileExcel, FileVideo, FileArchive, FileAlt, DownloadOutline,
    InformationCircleOutline
  },
  props: ['courseId'],
  setup(props) {
    const data = ref([])
    const message = useMessage()
    const loadingBar = useLoadingBar()
    const store = useStore()
    const loadingFlag = ref(false)

    const expandedKeys = ref([])
    const checkedKeys = ref([])
    const showDropdown = ref(false)
    const dropdownOptions = ref([
      {
        label: '下载此资源',
        key: 'download',
        itemInfo: {},
        icon() {
          return h(NIcon, null, {
            default: () => h(DownloadOutline)
          })
        },
      },
      {
        label: '查看此资源信息',
        key: 'viewResourceInfo',
        itemInfo: {},
        icon() {
          return h(NIcon, null, {
            default: () => h(InformationCircleOutline)
          })
        },
      }
    ])
    const posX = ref(0)
    const posY = ref(0)
    const showModal = ref(false)
    const modelData = ref({fileName: '', size: '', fileTitle: ''})

    const nameToIcon = {
      'folder': [Folder, '#f4d16e'],
      'pdf': [FilePdf, '#9e2a22'],
      'powerpoint': [FilePowerpoint, '#e18a3b'],
      'word': [FileWord, '#4994c4'],
      'excel': [FileExcel, '#4c8045'],
      'video': [FileVideo, '#0cca8a'],
      'zip': [FileArchive, '#ffc757']
    }

    function typeNameToSuffix(name) {
      return name in nameToIcon ? () => h(NIcon, {
        component: nameToIcon[name][0],
        color: nameToIcon[name][1]
      }) : () => h(NIcon, {component: FileAlt, color: '#686a67'})
    }

    function addSuffix(items) {
      items.forEach(item => {
        item.suffix = typeNameToSuffix(item['type_name'])
        if (item?.children?.length) {
          addSuffix(item.children)
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
          addSuffix(resData)

          resolve(resData)
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          resolve([])
        })
      })
    }

    const dropDownSelectFn = {
      async download(itemInfo) {
        let path = await window.$electron.utils.app.getPath('downloads')
        // 检查是否存在文件夹，不存在则创建
        path = window.$electron.utils.mkDir(path, 'Course Helper')
        common.showLoading(loadingFlag)

        const res = await window.$electron.utils.dialog.showOpenDialog({
          title: '请选择下载目录',
          defaultPath: path,
          properties: ['openDirectory']
        })
        if (!res?.filePaths?.length) {
          common.sendMsg(message, '未选择下载目录', 'error')
          common.hideLoading(loadingFlag)
          return
        }

        const dirPath = res.filePaths[0]
        api.post('http://127.0.0.1:6498/course/downloadCourseFiles', {
          file_list: [{
            file_id: itemInfo.file_id,
            res_id: itemInfo.res_id
          }],
          dir_path: dirPath
        }).then(res => {
          store.dispatch('push_download_queue', res.data)
          common.sendMsg(message, res.msg, 'success')
          common.hideLoading(loadingFlag)
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          common.hideLoading(loadingFlag)
        })
      },
      viewResourceInfo(itemInfo) {
        common.showLoading(loadingFlag)
        api.get(`http://127.0.0.1:6498/course/getCourseResourceInfo`, {
          file_id: itemInfo.file_id,
          res_id: itemInfo.res_id
        }).then(res => {
          modelData.value = {
            fileName: res.data['file_name'],
            size: res.data['file_size'],
            fileTitle: itemInfo['res_name']
          }
          showModal.value = true
          common.hideLoading(loadingFlag)
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          common.hideLoading(loadingFlag)
        })
      }
    }

    return {
      data,
      loadingFlag,
      pattern: ref(""),
      expandedKeys,
      checkedKeys,
      posX,
      posY,
      showDropdown,
      dropdownOptions,
      showModal,
      modelData,
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
      treeNodeProps({option}) {
        return {
          onContextmenu(e) {
            if (option['type_name'] !== 'folder') {
              const itemInfo = {
                key: option.key,
                res_id: option.res_id,
                file_id: option.file_id,
                res_name: option.res_name
              }
              dropdownOptions.value.forEach(item => {
                item['itemInfo'] = itemInfo
              })
              showDropdown.value = true
              posX.value = e.clientX
              posY.value = e.clientY
            }
            e.preventDefault()
          }
        }
      },
      handleSelect(key, options) {
        dropDownSelectFn[key](options.itemInfo)
        showDropdown.value = false
      },
      handleClickOutside() {
        showDropdown.value = false
      },
      downloadSelected() {
        console.log('下载所有选中项目， 通过store加key到资源列表内', checkedKeys.value)
      }
    }
  }
}
</script>

<style scoped>

</style>
