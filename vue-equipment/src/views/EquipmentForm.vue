
<template>
  <!-- Form Start -->
  <div class="container-fluid pt-4 px-4">
    <div class="row g-4">
      <div class="col-sm-12 col-xl-8">
        <div class="bg-light rounded h-100 p-4">
          <h6 class="mb-4">Оборудование</h6>
          <form>
            <div class="mb-3">
              <label for="serialNumberInputId" class="form-label">Серийный номер</label>
              <input type="text" class="form-control" id="serialNumberInputId"
                     aria-describedby="snHelp" v-model="equipmentItem.serial_number">
              <div id="snHelp" class="form-text">Серийный номер должен соответствовать маске типа оборудования
              </div>
            </div>
            <div class="mb-3">
              <label for="noteInputId" class="form-label">Примечание</label>
              <input type="text" class="form-control" id="noteInputId" v-model="equipmentItem.note">
            </div>

            <input type="hidden" class="form-control" id="eqTypeId" v-model="equipmentItem.equipment_type">

            <div class="mb-3">
              <label for="eqTypeSelectId" class="form-label">Тип оборудования</label>
              <select class="form-select form-select-lg mb-3" aria-label=".form-select-lg example"
                      id="eqTypeSelectId" @change="changeType($event)">
                <option v-for="type in this.store.state.equipmentTypes"
                        :selected="type.id === equipmentItem.equipment_type" :value="type.id">{{type.type_title}}</option>
              </select>
            </div>

            <button type="submit" class="btn btn-primary m-2" @click.prevent="updateEquipment()">Сохранить</button>
            <button type="submit" class="btn btn-danger m-2" @click.prevent="deleteEquipment()">Удалить</button>


          </form>
        </div>
      </div>
    </div>
  </div>
  <!-- Form End -->
</template>

<script>
import store from "../store";
export default {
  name: "EquipmentForm",
  props: ['id'],
  data(){
    return {
      equipmentItem: {}
    }
  },
  computed: {
    store() {
      return store
    }
  },
  created() {
    this.loadEquipmentItem()
  },
  methods: {
    async loadEquipmentItem(){
      let id_item = this.id
      const backendUrl = this.store.getters.getServerUrl + '/equipment/' + id_item
      const result = await fetch(backendUrl,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.store.state.accessToken}`
        }
      }).then(response => response.json())
      this.equipmentItem = result
    },
    async updateEquipment(){
      let id_item = this.id
      const backendUrl = this.store.getters.getServerUrl + '/equipment/' + id_item + "/"
      const result = await fetch(
          backendUrl, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.store.state.accessToken}`
            },
            body: JSON.stringify(this.equipmentItem)
          }
      // ).then(() => {
      //   this.$router.push({ name: 'home' })
      // })
      ).then(response => response.json())
    },
    async deleteEquipment() {
      let id_item = this.id
      const backendUrl = this.store.getters.getServerUrl + '/equipment/' + id_item + "/"
      const result = await fetch(
          backendUrl, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.store.state.accessToken}`
            },
            body: JSON.stringify(this.equipmentItem)
          }
      ).then(() => {
        this.$router.push({name: 'home'})
      })
    },
    changeType(event) {
      this.equipmentItem.equipment_type = event.target.value
    }
  }

}
</script>

<style scoped>

</style>