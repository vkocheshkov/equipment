import {createRouter, createWebHashHistory, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EquipmentForm from "@/views/EquipmentForm.vue";
import EquipmentCreationForm from "@/views/EquipmentCreationForm.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/:id',
    name: 'EquipmentForm',
    component: EquipmentForm,
    props: true
  },
  {
    path: '/add',
    name: 'add',
    component: EquipmentCreationForm,
  },
  {
    path: "/:catchAll(.*)",
    redirect: {name: 'home'}
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
