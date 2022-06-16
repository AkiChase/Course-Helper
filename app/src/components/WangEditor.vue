<template>
  <div style="border: 2px #eee solid">
    <Toolbar
        :editor="editorRef"
        :defaultConfig="toolbarConfig"
    />
    <Editor
        style="height:400px"
        v-model="valueHtml"
        :defaultConfig="editorConfig"
        @onCreated="handleCreated"
    />
  </div>
</template>

<script>
import '@wangeditor/editor/dist/css/style.css'
import {onBeforeUnmount, ref, shallowRef} from 'vue'
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";
import {useMessage} from "naive-ui";
import common from "@/utils/common";
import api from "@/utils/api";


export default {
  name: "WangEditor",
  components: {
    Editor, Toolbar
  },
  setup() {
    const editorRef = shallowRef()
    const valueHtml = ref('')
    const message = useMessage()

    //菜单配置
    const toolbarConfig = {
      excludeKeys: ['group-video', 'emotion', 'fullScreen'],
      insertKeys: {
        index: 23,
        keys: ['uploadAttachment', 'insertVideo']
      }
    }
    // 编辑器配置
    const editorConfig = {placeholder: '请输入内容...', MENU_CONF: {}}

    //插入链接配置
    editorConfig.MENU_CONF['insertLink'] = {
      checkLink(text, url) {
        if (!url) return
        if (url.indexOf('http') !== 0) {
          common.sendMsg(message, '链接必须以 http/https 开头', 'error')
          return
        }
        return true
      }
    }

    //图片配置
    editorConfig.MENU_CONF['uploadImage'] = {
      server: 'http://127.0.0.1:6498/file/uploadFile',
      base64LimitSize: 1024 * 1024,//1M内使用base64
      maxFileSize: 1024 * 1024 * 1024, // 网站的最大文件大小为1024M

      async customUpload(file, insertFn) {
        const msg = common.sendMsg(message, '图片大小超出 1M ，正在上传...', 'loading', 0)
        api.post('http://127.0.0.1:6498/file/uploadFile', {
          file_path: file.path
        }, 60000).then(res => {
          insertFn(res.data['file_url'], res.data['file_name'])
          msg.destroy()
          common.sendMsg(message, res.msg, 'success')
        }).catch(err => {
          msg.destroy()
          common.sendMsg(message, err, 'error')
        })
      },
    }

    //附件配置
    editorConfig.MENU_CONF['uploadAttachment'] = {
      server: 'http://127.0.0.1:6498/file/uploadFile',
      maxFileSize: 1024 * 1024 * 1024, // 网站的最大文件大小为1024M

      async customUpload(file, insertFn) {
        const msg = common.sendMsg(message, `正在上传附件...`, 'loading', 0)
        api.post('http://127.0.0.1:6498/file/uploadFile', {
          file_path: file.path
        }, 5 * 60000).then(res => {
          insertFn(res.data['file_name'], res.data['file_url'])
          msg.destroy()
          common.sendMsg(message, res.msg, 'success')
        }).catch(err => {
          msg.destroy()
          common.sendMsg(message, err, 'error')
        })
      },
    }


    // 组件销毁时，也及时销毁编辑器
    onBeforeUnmount(() => {
      const editor = editorRef.value
      if (editor == null) return
      editor.destroy()
    })


    return {
      editorRef,
      valueHtml,
      toolbarConfig,
      editorConfig,
      handleCreated(editor) {
        editorRef.value = editor // 记录 editor 实例，重要！
      },
      loadCustomHtml(html) {
        const left = html.indexOf('<!--GK&S-mJ包裹上限-->')
        const right = html.indexOf('<!--包裹下限&Mtf2Uj+.z-->')
        if (left === -1 || right === -1) {
          valueHtml.value = html
        } else {
          valueHtml.value = html.slice(left, right)
        }
      },
      getCustomHtml() {
        //对编辑器的html进行修改，用于上传course
        let html = '<div id="editor-content-view"><!--GK&S-mJ包裹上限-->' + valueHtml.value + '<!--包裹下限&Mtf2Uj+.z--></div>'
        html = html.replaceAll(/<span data-w-e-type="attachment".*?data-link=".*?openFile\/(.*?)".*?>(.*?)<\/span>/g,
            `<a class="attachment" href="/meol/common/ckeditor/openfile.jsp?id=$1">$2</a>`)
        html = html.replaceAll(/(<img.*?src=").*?openFile\/(.*?)"(.*?)>/g,
            `$1/meol/common/ckeditor/openfile.jsp?id=$2"$3`)

        html += `
<style>
${html.indexOf('<a class="attachment"')===-1? '': '#editor-content-view a.attachment{display:inline-block;margin-left:3px;margin-right:3px;border:2px solid transparent;border-radius:3px;padding:0 3px;background-color:#f1f1f1;cursor:inherit;text-decoration:none;color:#666}#editor-content-view a.attachment:hover{background-color:#ddd}#editor-content-view a.attachment:before{content:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20viewBox%3D%220%200%2024%2024%22%3E%3Cg%20fill%3D%22none%22%3E%3Cpath%20d%3D%22M16%202a6%206%200%200%201%204.397%2010.084l-.19.194l-8.727%208.727l-.053.05l-.056.045a3.721%203.721%200%200%201-5.253-5.242l.149-.164l.015-.011l7.29-7.304a1%201%200%200%201%201.416%201.413l-7.29%207.304l-.012.008a1.721%201.721%200%200%200%202.289%202.553l.122-.1l.001.001l8.702-8.7l.159-.165a4%204%200%200%200-5.753-5.554l-.155.16l-.018.012l-9.326%209.33a1%201%200%200%201-1.414-1.415l9.309-9.313l.046-.043A5.985%205.985%200%200%201%2016.001%202z%22%20fill%3D%22currentColor%22%3E%3C%2Fpath%3E%3C%2Fg%3E%3C%2Fsvg%3E");display:inline-block;width:12px;margin-right:5px}'}
#editor-content-view p,
#editor-content-view li {
  white-space: pre-wrap;
}
#editor-content-view blockquote {
  border-left: 8px solid #d0e5f2;
  padding: 10px 10px;
  margin: 10px 0;
  background-color: #f1f1f1;
}
#editor-content-view code {
  font-family: monospace;
  background-color: #eee;
  padding: 3px;
  border-radius: 3px;
}
#editor-content-view pre>code {
  display: block;
  padding: 10px;
}
#editor-content-view table {
  border-collapse: collapse;
}
#editor-content-view td,
#editor-content-view th {
  border: 1px solid #ccc;
  min-width: 50px;
  height: 20px;
}
#editor-content-view th {
  background-color: #f1f1f1;
}
#editor-content-view ul,
#editor-content-view ol {
  padding-left: 20px;
}
#editor-content-view input[type="checkbox"] {
  margin-right: 5px;
}
#editor-content-view [data-w-e-type="video"] {
  text-align: center;
}
</style>`
        return html
      }
    }
  }
}
</script>

<style scoped>

</style>
