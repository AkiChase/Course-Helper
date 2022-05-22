import {contextBridge, ipcRenderer} from 'electron'
import path from "path";
import fs from "fs";

const Store = require('electron-store');
const electronStore = new Store()


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
        },
        utils: {
            mkDir: (...args) => {
                const finalPath = path.join(...args)
                if (!fs.existsSync(finalPath)) fs.mkdirSync(finalPath, {recursive: true})
                return finalPath
            },
            fExists: (path) => fs.existsSync(path),
            shell: {
                showItemInFolder: async (path) => await ipcRenderer.invoke('shell:showItemInFolder', path)
            },
            app: {
                getPath: async (name) => await ipcRenderer.invoke('app:getPath', name),
                getFileIcon: async (filePath) => await ipcRenderer.invoke('app:getFileIconUrl', filePath),
            },
            dialog: {
                showOpenDialog: async (options) => await ipcRenderer.invoke('dialog:showOpenDialog', options)
            }
        }
    }
)
