const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    pluginOptions: {
        electronBuilder: {
            preload: "src/preload.js",
            builderOptions: {
                "appId": "com.ruchuby.course",
                "productName": "CourseHelper",
                "win": {
                    "icon": "dist_electron/icons/logo.ico"
                },
                "nsis": {
                    "oneClick": false,
                    "perMachine": true,
                    "allowElevation": true,
                    "allowToChangeInstallationDirectory": true,
                    "createDesktopShortcut": true
                }
            }
        }
    }
})
