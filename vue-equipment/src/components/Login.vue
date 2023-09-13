
<template>
  <div class="container-fluid">
    <div class="row h-100 align-items-center justify-content-center" style="min-height: 100vh;">
      <div class="col-12 col-sm-8 col-md-6 col-lg-5 col-xl-4">
        <div class="bg-light rounded p-4 p-sm-5 my-4 mx-3">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <a href="" class="">
              <h3 class="text-primary"><i class="fa fa-hashtag me-2"></i>Equipment</h3>
            </a>
            <h3>Sign In</h3>
          </div>
          <div class="form-floating mb-3">
            <input type="text" class="form-control" id="floatingInput" placeholder="Enter your login" v-model="username">
            <label for="floatingInput">Login</label>
          </div>
          <div class="form-floating mb-4">
            <input type="password" class="form-control" id="floatingPassword" placeholder="Password" v-model="password">
            <label for="floatingPassword">Password</label>
          </div>
          <p v-if="incorrectAuth">Неверные логин и пароль, попробуйте ввести заново</p>
          <br>
          <button type="submit" class="btn btn-primary py-3 w-100 mb-4" @click="login">Sign In</button>
          <p class="text-center mb-0">Don't have an Account? <a href="">Sign Up</a></p>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import store from "@/store";

export default {
  name: "Login",
  data(){
    return{
      username: '',
      password: '',
      incorrectAuth: false,
    }
  },
  computed: {
    store() {
      return store
    }
  },
  methods:{
    login () {
      this.store.dispatch('userLogin', {
        username: this.username,
        password: this.password
      })
          .then(() => {
            this.$router.push({ name: 'home' })
          })
          .catch(err => {
            console.log(err)
            this.incorrectAuth = true
          })
    }
  },
}
</script>

<style scoped>

</style>