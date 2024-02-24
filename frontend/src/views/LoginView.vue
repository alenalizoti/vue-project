<template>
    <div class="parent">
    
    <form>
        <h2>Log in</h2>
        {{ greska }}
        <p>
            <label>Username</label>
            <input type="text" v-model="user.username">
        </p>
        <p>
            <label>Password</label>
            <input type="password" v-model="user.password">
        </p>

        <p>
            <button @click.prevent="loginuj_korisnika" class="btn btn-primary">Log in</button>
            <button class="btn btn-danger"><router-link to="/">Cancel</router-link></button>
        </p>
    </form>
  </div>
</template>


<script>
import axios from 'axios';

export default{
    data(){
        return {
            user : {
                username : '',
                password : ''
            },
            greska : ''
          
        }
    },
    methods : {
        loginuj_korisnika(){
            if(this.user.username == "" || this.user.password == ""){
                this.greska = "Popunite sva polja!"
            }
            axios.post('http://127.0.0.1:5000/login', {
                username : this.user.username,
                password : this.user.password
            })
            .then((response) => {
                console.log(response);
                this.greska = '';
                this.user = response.data.data;
                // console.log(this.user)
                localStorage.setItem('username', JSON.stringify(this.user.username))
                localStorage.setItem('role', JSON.stringify(this.user.tip_korisnika))
                localStorage.setItem('id', JSON.stringify(this.user.id))
                this.$router.push({name:'home'})
            })
            .catch((error) => {
                console.log(error);
                this.greska = error.response.data.message;
            })
        }
    },
    beforeCreate(){
        const stored_data = localStorage.getItem('username')
        if(stored_data){
            this.$router.push({name: 'home'})
        }
    }
}

</script>

<style scoped>
    *{
        margin: 0;
        padding: 0;
    }
    .parent{
        height: 100vh;
        background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),url('../../public/images/poazdina_register.jpg');
        background-size:cover ;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    form{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 30em;
        margin: 0 auto;
        padding: 1em;
        border-radius: 10px;
        gap: 1em;
        background-color: rgba(139, 69, 19, 0.8);
    }
    form p{
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    label{
        color: #fff;
    }
    input{
        height: 2.2em;
        border-radius: 5px;
        width: 110%;
        border: none;
        padding-left: 1em;
    }
    select{
        width: 8em;
        height: 2em;
    }
    button{
        width: 7em;
        margin-top: 1em;
        height: 2.3em;
    }
    .image{
        display: flex;
        justify-content: center;
        width: 15em;
    }
    h2{
        color: #fff;
    }
    a{
        color: #fff;
        text-decoration: none;
    }
</style>