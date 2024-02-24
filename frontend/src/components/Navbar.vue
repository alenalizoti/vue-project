<template>
     <nav class="navbar navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
            <a class="navbar-brand" href="#">CoffeWorld</a>
            </div>
            <ul class="nav navbar-nav">
                <li ><router-link to="/">Pocetna</router-link></li>
                <li><router-link v-if="user.role == 'admin' || user.role == 'kupac'" to="/proizvodi">Proizvodi</router-link></li>
                <li><router-link v-if="user.role == 'prodavac'" :to="`/prodavac/` + user.username">Moji proizvodi</router-link></li>
                <li><router-link v-if="user.role == 'admin'" to="/admin/users">Svi korisnici</router-link></li>
            </ul>
            <ul v-if="chekIfLogged" class="nav navbar-nav navbar-right">
                <li><router-link to="/register"><span class="glyphicon glyphicon-user"></span> Sign Up</router-link></li>
                <li><router-link to="/login"><span class="glyphicon glyphicon-log-in"></span> Login</router-link></li>
            </ul>
            <ul v-else class="nav navbar-nav navbar-right">
                <li v-if="user.role =='kupac'"><router-link :to="`/cart/`+user.id"><i class="fas fa-shopping-cart korpa"></i></router-link></li>
                <li><router-link :to="'/profil/' + user.username"><span class="glyphicon glyphicon-user"></span> {{ user.username }}</router-link></li>
                <li><router-link to="/"><span class="glyphicon glyphicon-log-in"></span><button @click="logout" class="dugme">Log out</button></router-link></li>
            </ul>
        </div>
    </nav>
</template>

<script>
// import { computed } from "vue";


export default {
    data(){
        return {
            user : {
                username : '',
                role : '',
                id : ''
            }
        }
    },
    computed : {
        chekIfLogged(){
            const stored_data = localStorage.getItem('username')
            const stored_data2 = localStorage.getItem('role')
            const stored_data3 = localStorage.getItem('id')
            if(stored_data){
                this.user.username = JSON.parse(stored_data)
                this.user.role = JSON.parse(stored_data2)
                this.user.id = JSON.parse(stored_data3)
                return false
            }
            return true
        }
    },
    methods : {
        logout(){
            localStorage.removeItem('username')
            localStorage.removeItem('role')
            location.reload()
            this.$router.push({path : '/login'})
            
        }
    }
}
</script>


<style scoped>
    .dugme{
        background: none;
        border: none;
    }
    .navbar{
        margin-bottom: 0;
    }
    .korpa{
        font-size: 1.5em;
        color: #9d9d9d;
    }
    .korpa:hover{
        cursor: pointer;
        color: #f3e5c3;
    }
</style>