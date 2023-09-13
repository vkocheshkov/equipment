<template>
  <div class="home">
    <!-- Sale & Revenue Start -->
    <div class="container-fluid pt-4 px-4">
      <div class="row g-4">
        <div class="col-sm-6 col-xl-4">
          <div class="bg-light rounded d-flex align-items-center justify-content-between p-4">
            <i class="fa fa-chart-line fa-3x text-primary"></i>
            <div class="ms-3">
              <p class="mb-2">Оборудование кол-во</p>
              <h6 class="mb-0">{{this.totalCount}}</h6>
            </div>
          </div>
        </div>
        <div class="col-sm-6 col-xl-4">
          <div class="bg-light rounded d-flex align-items-center justify-content-between p-4">
            <i class="fa fa-chart-bar fa-3x text-primary"></i>
            <div class="ms-3">
              <p class="mb-2">Типы оборудования</p>
              <h6 class="mb-0">{{this.store.state.equipmentTypes.length}}</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Sale & Revenue End -->

    <!-- Recent Sales Start -->
    <div class="container-fluid pt-4 px-4" >
      <div class="bg-light text-center rounded p-4" v-if="this.equipmentList.length > 0">
        <div class="d-flex align-items-center ">

          <h6 class="mb-2">Доступное оборудование</h6>

          <form class="d-none d-md-flex ms-4 mb-2">
            <input class="form-control border-0" type="search" placeholder="Search" v-model="searchFor"
                   @keydown.enter.prevent="loadEquipment(this.current_page)">
          </form>
          <select class="form-select-pages mb-1" style="margin-left: auto; margin-right: 10px;" v-model="page_size" @change="loadEquipment(1)">
<!--            <option selected value="0">Все</option>-->
            <option selected value="5">5</option>
            <option value="15">15</option>
            <option value="30">30</option>
          </select>

        </div>
        <div class="table-responsive">
          <table class="table text-start align-middle table-bordered table-hover mb-0">
            <thead>
            <tr class="text-dark">
              <th scope="col">ID</th>
              <th scope="col">Серийный номер</th>
              <th scope="col">Тип оборудования</th>
              <th scope="col">Примечание</th>
              <th scope="col">Дата добавления</th>
              <th scope="col">Дата обновления</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="equipment in this.equipmentList" :key="equipment.id">
              <td>
                <router-link :to="{name: 'EquipmentForm', params:{id: equipment.id}}">{{equipment.id}}</router-link>
              </td>
              <td>{{equipment.serial_number}}</td>
              <td>{{this.getEquipmentType(equipment.equipment_type)}}</td>
              <td>{{equipment.note}}</td>
              <td>{{equipment.created_at}}</td>
              <td>{{equipment.updated_at}}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="bg-light p-4" v-else>
        <h3>Нет данных</h3>
      </div>
      <div class="col-sm-12 col-xl-12" v-if="pages !== 0">
        <div class="bg-light rounded h-100 p-4">
          <div class="btn-toolbar" role="toolbar">
            <div class="btn-group me-2" role="group" aria-label="First group">

              <button type="button" class="btn btn-primary" v-if="previous_page !== null"
                      @click="loadEquipment(current_page-1)">Назад</button>
              <template v-for="i in pages" :key="i">
                <button type="button" class="btn btn-primary" v-if="i <current_page+3 & i > current_page-3"
                        @click="loadEquipment(i)">{{ i }}</button>
              </template>
              <button type="button" class="btn btn-primary" v-if="next_page !== null"
                      @click="loadEquipment(current_page+1)">Вперед</button>
            </div>
          </div>
        </div>
      </div>

    </div>
    <!-- Recent Sales End -->
  </div>
</template>

<script>
import store from "../store";

export default {
  name: 'HomeView',
  data(){
    return {
      searchFor: '',
      equipmentList: [],
      page_size: 5,
      pages: 0,
      next_page: null,
      previous_page: null,
      current_page: 1,
      totalCount: 0
    }
  },
  computed: {
    store() {
      return store
    }
  },
  components: {},
  created() {
    this.loadEquipment(this.current_page)
    this.loadEquipmentTypes()
  },
  methods: {
    async loadEquipment(page) {
      this.current_page = page
      let server_url = this.store.state.backendUrl+ '/equipment/'
      let searchFor = '?search=' + this.searchFor + '&page_size=' + this.page_size + '&p=' + page
      let backendUrl = server_url + searchFor
      try {
        const response = await fetch(backendUrl,{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.store.state.accessToken}`
          }
        })
        if (response.status === 200) {
          let result = await response.json()
          this.equipmentList = result.results
          this.processPaginationData(result)
        }
      } catch (err) {
        console.log(err);
      }
    },
    loadEquipmentTypes () {

      this.store.dispatch('loadEquipmentTypes')
          .catch(err => {
            console.log(err)
          })
    },

    getEquipmentType(id){
      let type = 'не определен'
      let equipmentTypes = this.store.state.equipmentTypes

      for (let i = 0; i < equipmentTypes.length; i++) {
        if (equipmentTypes[i].id === id){
          type = equipmentTypes[i].type_title
          break
        }
      }
      return type
    },
    processPaginationData(data){
      this.totalCount = data.count
      this.pages = this.getNumberOfPages()
      this.next_page = data.next
      this.previous_page = data.previous
      console.log(this.previous_page)
      console.log(this.next_page)
    },
    getNumberOfPages(){
      return this.totalCount % this.page_size !== 0 && this.totalCount > this.page_size ?
          Math.floor(this.totalCount / this.page_size) + 1 : Math.floor(this.totalCount / this.page_size)
    }
  }
}
</script>
<style>
.form-select-pages {
  display: block;
  width: 80px;
  padding: .375rem 2.25rem .375rem .75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #757575;
  background-color: #fff;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right .75rem center;
  background-size: 16px 12px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  appearance: none
}
</style>
