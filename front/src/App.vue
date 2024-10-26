<template>
  <v-app>
    <v-main>
      <MainPage />
      <div class="alerts adaptive-alerts">
        <v-alert
          id="error-alert"
          class="alert-hidden adaptive-alert"
          type="error"
          @click="hideAppAlert('error')"
        >
        </v-alert>
        <v-alert
          id="warning-alert"
          class="alert-hidden adaptive-alert"
          type="warning"
          @click="hideAppAlert('warning')"
        ></v-alert>
        <v-alert
          id="info-alert"
          class="alert-hidden adaptive-alert"
          type="info"
          @click="hideAppAlert('info')"
        ></v-alert>
        <v-alert
          id="success-alert"
          class="alert-hidden adaptive-alert"
          type="success"
          @click="hideAppAlert('success')"
        ></v-alert>
      </div>
    </v-main>

  </v-app>
</template>

<script>
  import {hideAlert} from "@/commons/alerts";
  import MainPage from "@/MainPage.vue";

  export default {
    name: 'App',
    components: {MainPage},
    methods: {
      // Скрыть оповещение
      hideAppAlert(type) {
        hideAlert(type)
      }
    }
  }
</script>

<style scoped>
  @import "./assets/css/alerts.css";
</style>
