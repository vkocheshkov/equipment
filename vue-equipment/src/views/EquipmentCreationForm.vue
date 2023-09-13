<template>
  <!-- Form Start -->
  <div class="container-fluid pt-4 px-4">
    <div class="row g-4">
      <div class="col-sm-12 col-xl-8">
        <div class="bg-light rounded h-100 p-4">
          <h6 class="mb-4">Оборудование</h6>
          <form>
            <div class="mb-3">
              <label for="floatingTextarea">Серийный номер</label>
              <textarea class="form-control"
                        id="floatingTextarea" v-model="serialNumber"></textarea>
              <div id="snHelp" class="form-text">Серийные номера можно вводить с разделителями: " ", ",", "/", ";"
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
      <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="isActiveError">
        <i class="fa fa-exclamation-circle me-2"></i>{{ errorMessage }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="releaseError()"></button>
      </div>
      <div class="alert alert-success alert-dismissible fade show" role="alert" v-if="isActiveMessage">
        <i class="fa fa-exclamation-circle me-2"></i>Серийные номера {{ informMessage }} успешно добавлены!
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="releaseMessage()"></button>
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
      isActiveError: false,
      isActiveMessage: false,
      errorMessage: null,
      informMessage: null

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
        "serial_numbers": this.serialNumber.split(/[;.,\/ ]/),
        "equipment_type": this.equipmentType,
        "note": this.note,
      }
      const backendUrl = this.store.getters.getServerUrl + '/equipment/'
      try {
      const response = await fetch(
          backendUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.store.state.accessToken}`
            },
            body: JSON.stringify(data)
          }
      )
        if (response.status === 201) {
          let result = await response.json()
          this.isActiveMessage = true
          this.informMessage = result["serial_numbers"]
        } else {
          let result = await response.json()
          this.isActiveError = true
          this.errorMessage = result["description"]
        }
      } catch (err) {
        console.log("Ошибка при добавлении серийного номера", err);
      }
    },
    releaseError(){
      this.isActiveError = false
      this.errorMessage = null
    },
    releaseMessage(){
      this.isActiveMessage = false
      this.informMessage = null
    }
  }
}
</script>

<style scoped>

</style>