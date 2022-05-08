'use strict'

import {app, protocol, BrowserWindow, screen} from 'electron'
import {createProtocol} from 'vue-cli-plugin-electron-builder/lib'
import path from 'path'

import ipcHelper from "@/utils/ipcHelper"


const isDevelopment = process.env.NODE_ENV !== 'production'

protocol.registerSchemesAsPrivileged([
    {scheme: 'app', privileges: {secure: true, standard: true}}
])


let win //全局 BrowserWindow

async function createWindow() {
    const screenArea = screen.getPrimaryDisplay().workAreaSize
    win = new BrowserWindow({
        width: Math.round(screenArea.width * 0.7),
        height: Math.round(screenArea.height * 0.9),
        frame: false, //关闭默认标题栏
        webPreferences: {
            preload: path.join(__dirname, "preload.js")
        }
    })

    const Store = require('electron-store');
    Store.initRenderer();


    if (process.env.WEBPACK_DEV_SERVER_URL) {
        // Load the url of the dev server if in development mode
        await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    } else {
        createProtocol('app')
        // Load the index.html when not in development
        await win.loadURL('app://./index.html')
    }

    win.webContents.openDevTools() //打开开发者工具
}

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

app.on('ready', () => {
    createWindow().then(() => {
        ipcHelper(win)
    })
})

if (isDevelopment) {
    if (process.platform === 'win32') {
        process.on('message', (data) => {
            if (data === 'graceful-exit') {
                app.quit()
            }
        })
    } else {
        process.on('SIGTERM', () => {
            app.quit()
        })
    }
}
