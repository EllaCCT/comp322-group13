import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('user', {
  state: () => ({    
    username: '',
    email: '',
    address: '',
    is_login: false,
    token: '',
  }),
  actions: {
    getMember(){
      axios.get('/getinfo/', {
        headers: {
          'Authorization': 'TOKEN ' + this.token,
        },          
      }).then((response) => {
        this.updateUser(response.data)
      }).catch((err) => console.log(err))        
    },
    updateJwt(token) {
      this.token = token
    },
    updateUser(userData) {
      this.username = userData.username
      this.email = userData.email
      this.address = userData.address
      this.is_login = true
    }
  }
})