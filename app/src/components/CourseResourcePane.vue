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

          virtual-scroll=""
          style="height: 45vh"
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
    <DownloadModal ref="downloadModalRef" :data="downloadModalData"/>
  </div>
</template>

<script>
import {
  NButton,
  NCard,
  NDropdown,
  NEllipsis,
  NIcon,
  NInput,
  NModal,
  NSpace,
  NSpin,
  NTooltip,
  NTree,
  useLoadingBar,
  useMessage
} from "naive-ui";
import {h, onMounted, ref} from "vue";
import api from "@/utils/api";
import common from "@/utils/common";
import {BulbOutline, DownloadOutline, InformationCircleOutline} from "@vicons/ionicons5";
import {FileAlt, FileArchive, FileExcel, FilePdf, FilePowerpoint, FileVideo, FileWord, Folder} from "@vicons/fa";
import {useStore} from "vuex";
import DownloadModal from "@/components/DownloadModal";

export default {
  name: "CourseResourcePane",
  components: {
    NInput, NTree, NButton, NSpace, NIcon, NTooltip, NDropdown, NModal, NCard, NSpin, NEllipsis,
    BulbOutline, Folder, FilePdf, FilePowerpoint, FileWord, FileExcel, FileVideo, FileArchive, FileAlt, DownloadOutline,
    InformationCircleOutline,
    DownloadModal
  },
  props: ['courseId', 'courseName'],
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

    const downloadModalRef = ref(null)
    const downloadModalData = ref({
      title: '新建下载任务',
      form: {
        dirPath: '',
        options: {
          treeFlag: false,
        }
      }
    })

    onMounted(async () => {
      let path = await window.$electron.utils.app.getPath('downloads')
      path = window.$electron.utils.mkDir(path, 'Course Helper')
      downloadModalData.value.form.dirPath = path
    })


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
    function findNode(tree, key) {
      if (tree.key === key) {
        return {path: [], node: tree}
      }

      if ('children' in tree) {
        for (let i = 0; i < tree.children.length; i++) {
          const res = findNode(tree.children[i], key)
          if (res !== null) {
            res.path.unshift(tree.children[i]['res_name'])
            return res
          }
        }
      }
      return null
    }

    function getDirPathInTree(keys, arr) {
      const out = {}
      keys.forEach(key => {
        const res = findNode({children: arr}, key)
        res.path.pop()
        out[key] = res
      })
      return out
    }

    const dropDownSelectFn = {
      download(itemInfo) {
        downloadModalData.value.form.options.treeFlag = false
        downloadModalRef.value.showDownloadModal().then(() => {
          const dirPath = downloadModalData.value.form.dirPath
          let fileDir = './'
          if (downloadModalData.value.form.options.treeFlag) {
            fileDir += `${props.courseName}/`
            // 解析目录结构
            const keyDirPath = getDirPathInTree([itemInfo.key], data.value)
            fileDir += keyDirPath[itemInfo.key].path.join('/')
          }

          common.showLoading(loadingFlag)
          api.post('http://127.0.0.1:6498/course/downloadCourseFiles', {
            file_list: [{
              file_id: itemInfo.file_id,
              res_id: itemInfo.res_id,
              file_dir: fileDir
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
        }).catch(e => {
          console.log(e)
          common.sendMsg(message, '下载取消', 'error')
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

    async function downloadSelected() {
      if (!checkedKeys.value.length) {
        common.sendMsg(message, '未选择任何项目', 'error')
        return
      }

      downloadModalData.value.form.options.treeFlag = true
      downloadModalRef.value.showDownloadModal().then(() => {
        const dirPath = downloadModalData.value.form.dirPath
        const fileList = []

        const keyDirPath = getDirPathInTree(checkedKeys.value, data.value)
        checkedKeys.value.forEach(key => {
          const node = keyDirPath[key].node
          fileList.push({
            file_id: node.file_id,
            res_id: node.res_id,
            file_dir: downloadModalData.value.form.options.treeFlag ?
                `./${props.courseName}/` + keyDirPath[key].path.join('/') : './'
          })
        })

        if (fileList.length > 5) {
          common.sendMsg(message, '下载文件数量较多(>5)，请耐心等待', 'info')
        }

        common.showLoading(loadingFlag)
        api.post('http://127.0.0.1:6498/course/downloadCourseFiles', {
          file_list: fileList,
          dir_path: dirPath
        }, fileList.length * 1000).then(res => {
          store.dispatch('push_download_queue', res.data)
          common.sendMsg(message, res.msg, 'success')
          common.hideLoading(loadingFlag)
        }).catch(err => {
          common.sendMsg(message, err, 'error')
          common.hideLoading(loadingFlag)
        })

      }).catch(e => {
        console.log(e)
        common.sendMsg(message, '下载取消', 'error')
      })
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
      downloadModalRef,
      downloadModalData,
      onLoad(node) {
        const folderId = node['folder_id']
        const courseId = props.courseId
        return load(courseId, folderId).then(res => {
          if (res.length) node.children = res
        })
      },
      preLoad(courseId) {
        // 重置已选资源
        checkedKeys.value = []
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
      downloadSelected
    }
  }
}
</script>

<style scoped>

</style>
