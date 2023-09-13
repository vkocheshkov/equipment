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
                     aria-describedby="snHelp" v-model="serialNumber">
              <div id="snHelp" class="form-text">Серийный номер должен соответствовать маске типа оборудования
              </div>
            </div>
            <div class="mb-3">
              <label for="noteInputId" class="form-label">Примечание</label>
              <input type="text" class="form-control" id="noteInputId" v-model="note">
            </div>

            <div class="mb-3">
              <label for="eqTypeSelectId" class="form-label">Тип оборудования</label>
              <select class="form-select mb-3" aria-label=".form-select-lg example"
                      id="eqTypeSelectId" v-model="equipmentType">
                <option v-for="type in this.store.state.equipmentTypes" :value="type.id">{{type.type_title}}</option>
              </select>
            </div>

            <button type="submit" class="btn btn-primary m-2" @click.prevent="addEquipment()">Сохранить</button>

          </form>
        </div>
      </div>
    </div>
  </div>
  <!-- Form End -->
</template>

<script>
import store from "@/store";

export default {
  name: "EquipmentCreationForm",
  data(){
    return {
      equipmentType: '',
      serialNumber: '',
      note: '',
    }
  },
  computed: {
    store() {
      return store
    }
  },
  created() {
  },
  methods: {
    async addEquipment(){
      let data = {
        "serial_number": this.serialNumber,
        "equipment_type": this.equipmentType,
        "note": this.note,
      }
      const backendUrl = this.store.getters.getServerUrl + '/equipment/'
      const result = await fetch(
          backendUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.store.state.accessToken}`
            },
            body: JSON.stringify(data)
          }
      ).then(this.$router.push({ name: 'home' })).catch((error) => {
        console.error(error);
      })
    },
  }
}
</script>

<style scoped>

</style>