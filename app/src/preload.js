import {contextBridge, ipcRenderer} from 'electron'
import wsHelper from "@/utils/wsHelper";


contextBridge.exposeInMainWorld('$electron', {
        win: {
            minimize: () => ipcRenderer.send('win:minimize'),
            maximize: () => ipcRenderer.send('win:maximize'),
            close: () => ipcRenderer.send('win:close'),
        },
    }
)

contextBridge.exposeInMainWorld('$ws', {
        ...wsHelper
    }
)
