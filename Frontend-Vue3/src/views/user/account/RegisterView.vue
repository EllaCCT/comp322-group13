<template>
  <section class="vh-100">
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-12 col-md-9 col-lg-7 col-xl-4">
          <div class="card" style="border-radius: 15px;">
            <div class="card-body p-5">
              <h2 class="text-center mb-5">Register page</h2>
              <form @submit.prevent="register">
                <div class="form-outline mb-4">
                  <label for="username">Username</label>
                  <input v-model="username" type="text" class="form-control form-control-lg" id="username" />                
                </div>
                <div class="form-outline mb-4">
                  <label for="password">Password</label>
                  <input v-model="password" type="password" class="form-control" id="password" />
                </div>
                <div class="form-outline mb-4">
                  <label for="confirm_password">Confirm password</label>
                  <input v-model="confirm_password" type="password" class="form-control" id="confirm_password" />
                </div> 
                <div class="error_message">{{ error_message }}</div>
                <div class="d-flex justify-content-center">             
                  <button type="submit" class="btn btn-primary btn-block">Submit</button>
                </div>                
                <p class="text-center text-muted mt-3">Already have account?
                  <router-link :to="{name: 'UserLogin'}"> 
                    <u>Login</u>
                  </router-link>                  
                </p>            
                <div class="debug">Testing <br/>Username:{{ username }} <br/> Password:{{ password }} <br/> Confirm password:{{ confirm_password }}</div>    
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default{
  data(){
    return{
      username: "",
      password: "",
      confirm_password: "",
      email: "",
      address: "",
      error_message:"",
    }
  },
  methods:{
    register(){
      this.$axios.post('/register/',{
      "username": this.username, 
      "password": this.password, 
      "confirm_password": this.confirm_password,
      "email": this.email,
      "address": this.address    
    }).then((response) => {
        console.log(response);
        if (response.data.message == "Registered successful."){
          this.$router.push({name:"Index"})
        } else {
          this.error_message = response.data.message
        }        
      })
      .catch((err) => console.log(err))
    }
  }
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