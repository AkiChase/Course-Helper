import {contextBridge, ipcRenderer} from 'electron'
import wsHelper from "@/utils/wsHelper";

const Store = require('electron-store');
const electronStore = new Store()
// electronStore.openInEditor()

contextBridge.exposeInMainWorld('$electron', {
        win: {
            minimize: () => ipcRenderer.send('win:minimize'),
            maximize: () => ipcRenderer.send('win:maximize'),
            close: () => ipcRenderer.send('win:close'),
        },
        store: {
            set: (key, val) => electronStore.set(key, val),
            del: (key) => electronStore.delete(key),
            get: (key, defaultValue = undefined) => electronStore.get(key, defaultValue),
            has: (key) => electronStore.has(key),
            setWithObj: (obj) => electronStore.set(obj)
        }
    }
)

contextBridge.exposeInMainWorld('$ws', {
        ...wsHelper
    }
)
