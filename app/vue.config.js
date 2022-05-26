const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    pluginOptions: {
        electronBuilder: {
            preload: "src/preload.js",
            builderOptions: {
                "appId": "com.ruchuby.course",
                "productName": "CourseHelper",
                "extraResources":[{
                    "from": "../server/dist/server.exe",
                    "to": "./server.exe",
                    "filter": ["**/*", "!foo/*.js"]
                }],
                "win": {
                    "icon": "dist_electron/icons/icon.png"
                },
                "nsis": {
                    "oneClick": false,
                    "allowElevation": true,
                    "allowToChangeInstallationDirectory": true,
                    "deleteAppDataOnUninstall":true,
                    "shortcutName":'course助手',
                    "installerIcon":'dist_electron/icons/installer.ico',
                    "uninstallerIcon":'dist_electron/icons/uninstaller.ico'
                }
            }
        }
    }
})
