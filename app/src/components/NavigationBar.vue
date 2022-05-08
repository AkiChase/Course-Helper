<template>
  <div class="main" :style="`background-color: ${themeVars.primaryColor}`">
    <div class="logo">
      <img src="../assets/logo.png" alt=""/>
    </div>

    <nav-button :to="{name:'login'}">
      <settings-outline/>
    </nav-button>
    <nav-button :to="{name:'home'}">
      <settings-outline/>
    </nav-button>

  </div>
</template>

<script>


import {useThemeVars} from "naive-ui";
import Login from "@/views/Login";
import NavButton from "@/components/NavButton";
import {SettingsOutline} from "@vicons/ionicons5";

export default {
  name: "NavigationBar",
  components: {
    Login,
    SettingsOutline,
    NavButton
  },
  setup() {
    const themeVars = useThemeVars()

    return {
      themeVars
    }
  }
}
</script>

<style scoped>
.main{
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo {
  padding: 0 10px;
}

.logo > img {
  width: 100%;
}
</style>
