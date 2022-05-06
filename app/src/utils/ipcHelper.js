import {ipcMain} from 'electron'

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

    ipcMain.handle('echo', async (e, ...args) => {
        console.log(args)
        return args
    })
}
