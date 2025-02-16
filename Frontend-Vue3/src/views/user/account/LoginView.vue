<template>
  <section class="vh-100">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-12 col-md-9 col-lg-7 col-xl-4">
          <div class="card" style="border-radius: 15px;">
            <div class="card-body p-5">
              <h2 class="text-center mb-5">Login page</h2>
              <form @submit.prevent="login">
                <div class="form-outline mb-4">
                  <label for="username">Username</label>
                  <input v-model="username" type="text" class="form-control form-control-lg" id="username" />                
                </div>
                <div class="form-outline mb-4">
                  <label for="password">Password</label>
                  <input v-model="password" type="password" class="form-control" id="password" />
                </div>                
                <div class="error_message">{{ error_message }}</div>
                <div class="d-flex justify-content-center">             
                  <button type="submit" class="btn btn-primary btn-block">Submit</button>
                </div>                
                <p class="text-center text-muted mt-3">Don't have an account yet?
                  <router-link :to="{name: 'UserRegister'}"> 
                    <u>Sign up</u>
                  </router-link>                  
                </p>            
                <div class="debug">Testing <br/>Username:{{ username }} <br/> Password:{{ password }} </div>    
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useUserStore } from '../../../stores/user';
import { ref,getCurrentInstance } from 'vue';
import { useRouter } from 'vue-router';

const userStore = useUserStore()
const {proxy} = getCurrentInstance()
const router = useRouter()

let username = ref("")
let password = ref("")
let error_message = ref("")

const login = () => {
  proxy.$axios.post("/login/",{
    "username": username.value, 
    "password": password.value, 
  }).then((response) => {
    if (response.data.message == "Login successful."){
      localStorage.setItem("jwt_token", response.data.jwt_token)
      userStore.updateJwt(response.data.jwt_token)
      userStore.getMember()
      router.push({name: "Index"})      
      } else {
        error_message.value = response.data.message
      }
    })
  } 
</script>

<style scoped>
  .error_message{
    color: red;
  }
  .debug{
    color:dodgerblue;
  }
</style>