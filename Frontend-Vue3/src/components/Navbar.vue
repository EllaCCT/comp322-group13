<template>
  <div class="wrapper">
    <div class="container d-flex justify-content-center">
      <div class="title">
        Hello!
        <div class="title-info">
          Here is a testing site!
          <div class="d-flex justify-content-center">
            <router-link :to="{name: 'UserLogin'}">
              <button type="button" class="btn btn-login">Login</button>
            </router-link>
            <router-link :to="{name: 'UserRegister'}">
              <button type="button" class="btn btn-register">Register</button>
            </router-link>
          </div>
        </div>
      </div>    
    </div>
  </div>
</template>

<script>

</script>

<style scoped>
.wrapper{
  background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(82,29,223,1) 100%);
}

.title{
  margin-top:40px;
  text-align: center;
  font-size:32px;
  color: white;
}

.title-info{
  padding: 4px;
  text-align:center;
  font-size: 16px;
}
</style>