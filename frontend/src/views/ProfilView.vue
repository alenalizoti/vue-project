<template>
    <div class="container main">
        <div class="profil">
            <div class="gore">
                <div class="opcija">
                    <img :src="`../public/users_images/` + user.username + tip_fajla" alt="profilna"> 
                    <router-link :to="`/update/${user.username}`">Izmeni</router-link>
                </div>
                <div class="name">
                    <h1>{{ user.username }}</h1>
                </div>
            </div>
            <div class="dole">
                <div class="podaci">
                    <p class="kljuc">Username:</p>
                    <p class="vrednost">{{ user.username }}</p>
                </div>
                <div class="podaci">
                    <p class="kljuc">Password:</p>
                    <p class="vrednost">{{ user.password }}</p>
                </div>
                <div class="podaci">
                    <p class="kljuc">Email:</p>
                    <p class="vrednost">{{ user.email }}</p>
                </div>
                <div class="podaci">
                    <p class="kljuc">Godina rodjenja:</p>
                    <p class="vrednost">{{ user.godiste }}</p>
                </div>
                <div class="podaci">
                    <p class="kljuc">Novac na racunu:</p>
                    <p class="vrednost">{{user.trenutno_stanje_novca}}</p>
                </div>
                <div class="podaci">
                    <p class="kljuc">Tip korisnika:</p>
                    <p class="vrednost">{{ user.tip_korisnika }}</p>
                </div>

            </div>
            
        </div>
        
        <div class="istorija-kupovina">
            <h2>Istorija kupovina</h2>
            <div v-for="proizvod in istorija" :key="proizvod.id" class="istorija">
                <div class="about">
                    <p>{{ proizvod.naziv }}</p>
                    <p>{{ proizvod.cena }}</p>
                </div>
                <div class="datum">
                    {{ proizvod.datum_kupovine }}
                </div>
            </div>
        </div>

       
    </div>
</template>



<script>
import axios from 'axios'


export default {
    data(){
        return {
            user : {},
            tip_fajla : '',
            id_korisnika : '',
            istorija : []
        }
    },
    props : ['username'],
    methods : {
        fechHistory(){
            axios.get(`http://127.0.0.1:5000/istorija/kupovina/${this.id_korisnika}`)
            .then((response) => {
                console.log(response);
                this.istorija = response.data.data2;
                console.log(this.istorija);
                console.log(typeof(this.istorija));
            })
            .catch((error) => {
                console.log(error);
            })
        },
        fechUserID(){
            const stored_data = localStorage.getItem('id')
            if(stored_data){
                this.id_korisnika = JSON.parse(stored_data)
                console.log(this.id_korisnika);
            }
        }
    },  
    mounted(){
        const username = this.username;
        axios.get(`http://127.0.0.1:5000/profil/${username}`)
        .then((response) => {
            this.user = response.data.data;
            this.tip_fajla = response.data.ext;
            this.fechHistory()
        })
        .catch((error) => {
            console.log(error);
        })
        this.fechUserID()
    },
    beforeCreate(){
        const stored_data = localStorage.getItem('username')
        if(stored_data){
            return true
        }
        this.$router.push({path : '/'})
    }
}
</script>

<style scoped>
    *{
        margin: 0;
        padding: 0;
        font-family: sans-serif;
    }
    .main{
        width: 100%;
        height: 95vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),url('../../public/images/poazdina_register.jpg');
        background-repeat: no-repeat;
        background-size: cover;
        gap: 2em;
    }
    .profil{
        /* margin: 0 auto; */
        width: 25em;
        display: flex;
        flex-direction: column;
        gap: 3em;
        padding: 1em;
        align-items: center;
        border-radius: 10px;
        background-color: rgba(139, 69, 19, 0.8);
    }
    .gore{
        display: flex;
        align-items: center;
        margin: 0 1em;
    }
    .opcija img{
        width: 40%;
        border-radius: 50%;
    }
    .opcija{
        display: flex;
        flex-direction: column;
    }
    a{
        margin-left: 0.5em;
        margin-top: 0.5em;
        color: #fff;
    }
    a:hover{
        text-decoration: none;
    }
    .podaci{
        display: flex;
        gap: 1em;
        margin-bottom: 2em;
    }
    .vrednost{
        font-weight: bold;
        font-size: 1.4em;
    }
    .kljuc{
        font-size: 1.4em;
    }
    p{
        color: #fff;
    }
    .name{
        color: #fff;
    }
    .about{
        display: flex;
        justify-content: space-between;
        font-size: 1.2em;
    }
    .datum{
        color: #fff;
        text-align: center;
        padding: 1em;
    }
</style>