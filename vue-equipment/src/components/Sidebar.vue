<template>
  <!-- Sidebar Start -->
  <div class="sidebar pe-4 pb-3">
    <nav class="navbar bg-light navbar-light">
      <a href="#" class="navbar-brand mx-4 mb-3">
        <h3 class="text-primary"><i class="fa fa-hashtag me-2"></i>EQUIPMENT</h3>
      </a>
      <div class="navbar-nav w-100">
        <router-link to="/" exact class="nav-item nav-link"><i class="fa fa-tachometer-alt me-2"></i>Оборудование</router-link>
        <router-link to="add" exact class="nav-item nav-link"><i class="fa fa-th me-2"></i>Добавить</router-link>
      </div>
    </nav>
  </div>
  <!-- Sidebar End -->
</template>
<script>

export default {
  name: "Sidebar"
}
</script>
<style scoped>


</style>