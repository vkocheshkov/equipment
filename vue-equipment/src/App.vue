<template>
  <div id="app">
    <div v-if="this.store.getters.loggedIn">
      <Sidebar />
      <div class="content">
        <Nav />
        <router-view />
      </div>
    </div>
    <div v-else>
      <Login />
    </div>
  </div>

</template>

<style>
  @import "assets/css/bootstrap.min.css";
  @import "assets/css/style.css";

</style>
<script>

import {defineComponent} from "vue";
import Nav from "@/components/Nav.vue";
import Sidebar from "@/components/Sidebar.vue";
import Login from "@/components/Login.vue";
import store from "@/store";

export default defineComponent({
  components: {Login, Sidebar, Nav},
  data() {
    return{
    }
  },
  computed: {
    store() {
      return store
    }
  },
})
</script>