import {ipcMain, dialog, app, shell} from 'electron'

export default (win) => {
    ipcMain.on('win:minimize', () => win.minimize())
    ipcMain.on('win:maximize', () => {
        if (win.isMaximized()) {
            win.unmaximize()
        } else {
            win.maximize()
        }
    })
    ipcMain.on('win:close', () => {
        win.destroy()
    })

    ipcMain.handle('dialog:showOpenDialog', async (e, options) => dialog.showOpenDialog(options))
    ipcMain.handle('app:getPath', async (e, name) => app.getPath(name))
    ipcMain.handle('app:getFileIconUrl', async (e, filePath) =>
        (await app.getFileIcon(filePath, {size: 'large'})).toDataURL())
    ipcMain.handle('shell:showItemInFolder', async (e, filePath) => shell.showItemInFolder(filePath))
}
