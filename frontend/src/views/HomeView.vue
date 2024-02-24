<template>
  <div class="main">
    <div v-if="!chekIfLogged" class="welcome">
      <h2>Dobrodosli na nas website</h2>
      <p>Ulogujte se kako bi videli proizvode</p>
      <div class="buttons">
        <button @click="goToLogin" class="btn btn-primary">Login</button>
        <button @click="goToRegister" class="btn btn-primary">Register</button>
      </div>
    </div>
    <div v-else class="welcome">
      <h2>{{username}} uspesno ste se ulogovali</h2>
      <p>Pogledajte proizvode na nasem sajtu...</p>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return {
      username : ''
    }
  },
  methods : {
    goToLogin(){
      this.$router.push({name : 'login'})
    },
    goToRegister(){
      this.$router.push({name : 'register'})
    }
  },
  computed : {
      chekIfLogged(){
          const stored_data = localStorage.getItem('username')
          if(stored_data){
              this.username = JSON.parse(stored_data)
              return true
          }
          return false
      }
    },
}
</script>

<style scoped>
  .main{
    height: 93vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),url('../../public/images/poazdina_register.jpg');
    background-size:cover ;
  }
  .welcome h2{
    font-size: 3em;
    color: #fff;
  }
  .welcome p {
    font-size: 1.5em;
    color: #fff;
    text-align: center;
  }
  .buttons{
    display: flex;
    justify-content: center;
    margin-top: 2em;
    gap: 2em;
  }
  .buttons button{
    font-size: 1.5em;
  }
</style> 
