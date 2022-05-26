import {app, dialog, ipcMain, shell} from 'electron'
import path from 'path'
import open from 'open'

export default (win) => {
    ipcMain.on('win:minimize', () => win.minimize())
    ipcMain.on('win:maximize', () => win.isMaximized() ? win.unmaximize() : win.maximize())
    ipcMain.on('win:close', () => win.destroy())
    ipcMain.on('win:devTools', () => win.webContents.isDevToolsOpened() ?
        win.webContents.closeDevTools() : win.webContents.openDevTools())

    ipcMain.handle('dialog:showOpenDialog', async (e, options) => dialog.showOpenDialog(options))

    ipcMain.handle('app:getPath', async (e, name) => app.getPath(name))
    ipcMain.handle('app:getFileIconUrl', async (e, filePath) =>
        (await app.getFileIcon(filePath, {size: 'large'})).toDataURL())

    ipcMain.handle('shell:showItemInFolder', async (e, filePath) => shell.showItemInFolder(filePath))

    ipcMain.handle('download:downloadURL', async (e, url) => win.webContents.downloadURL(url))

    ipcMain.handle('open:server', async (e, cmd) => {
        const serverPath = process.env.NODE_ENV !== 'production' ?
            path.join(__dirname, "../../server/dist/server.exe") : path.join(process.cwd(), "/resources/server.exe")
        await open.openApp(serverPath, {arguments: [cmd]})
    })
}
