<template>
  <div class="parent">
    
    <form>
        <h2>Registracija</h2>
        {{ provera }}
        <p>
            <label>Username</label>
            <input type="text" v-model="korisnik.username">
            <span class="greska" v-if="greska.username">{{ greska.username }}</span>
        </p>
        <p>
            <label>Password</label>
            <input type="password" v-model="korisnik.password">
            <span class="greska" v-if="greska.password">{{ greska.password }}</span>
        </p>
        <p>
            <label>Confirm password</label>
            <input type="password" v-model="korisnik.confirm_password">
            <span class="greska" v-if="greska.confirm_password">{{ greska.confirm_password }}</span>
        </p>
        <p>
            <label>Email</label>
            <input type="email" v-model="korisnik.email">
            <span class="greska" v-if="greska.email">{{ greska.email }}</span>
        </p>
        <p>
            <label>Godina rodjenja</label>
            <input type="number" v-model="korisnik.godiste">
            <span class="greska" v-if="greska.godiste">{{ greska.godiste }}</span>
        </p>
        <p>
            <label>Profilna slika</label>
            <input class="image" type="file" @change="handleFileChange" ref="image_file">
            <span class="greska" v-if="greska.putanja_img">{{ greska.putanja_img }}</span>
        </p>
        <p>
            <label>Trenutno stanje nova</label>
            <input type="text" v-model="korisnik.stanje_novca" readonly>    
        </p>
        <p>
            <label>Vrsta korisnika</label>
            <select v-model="korisnik.vrsta_korisnika">
                <option value="" selected>Izaberite...</option>
                <option value="prodavac">Prodavac</option>
                <option value="kupac">Kupac</option>
            </select>
            <span class="greska" v-if="greska.vrsta_korisnika">{{ greska.vrsta_korisnika }}</span>
        </p>

        <p>
            <button @click.prevent="register" class="btn btn-primary">Register</button>
            <button class="btn btn-danger"><router-link to="/">Cancel</router-link></button>
        </p>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    data(){
        return{
            korisnik : {
                username : '',
                password : '',
                confirm_password : '',
                email : '',
                godiste : '',
                putanja_img : '',
                stanje_novca : 0,
                vrsta_korisnika : ''
            },
            greska : {
                username : '',
                password : '',
                confirm_password : '',
                email : '',
                godiste : '',
                putanja_img : '',
                vrsta_korisnika : ''
            },
            provera : ""

        }
    },
    methods : {
        handleFileChange(){
            const fileInput = this.$refs.image_file;
            var file = null
            if (fileInput.files.length > 0){
                file = fileInput.files[0]
            }
            const reader = new FileReader();
            reader.onloadend = () => {
                this.korisnik.putanja_img = reader.result.split(',')[1]
            }

            reader.readAsDataURL(file)
        },
        register(){
            if(this.korisnik.username == "" || this.korisnik.password == "" || this.korisnik.confirm_password == "" || this.korisnik.email == "" || this.korisnik.godiste == ""  || this.korisnik.vrsta_korisnika == "" ){
                
                return this.provera = "Niste popunili sva polja"
            }
            if(this.korisnik.username.length < 3){
                return this.greska.username = "Minimalan unos je 3 karaktera"
            }
            else if(this.korisnik.password.length < 5){
                return this.greska.password = "Minimalan unos je 5 karaktera"
            }
            else if(this.korisnik.password != this.korisnik.confirm_password){
                return this.greska.confirm_password = "Lozinke se ne poklapaju"
            }
            else if(!this.korisnik.email.includes("@") || !this.korisnik.email.includes(".")){
                return this.greska.email = "Email mora da sadrzi @ i ."
            }
            else if (this.korisnik.godiste < 1900 || this.korisnik.godiste > 2024){
                return this.greska.godiste = 'Unos nije validan!'
            }

            this.greska = {
                username : '',
                password : '',
                confirm_password : '',
                email : '',
                godiste : '',
                putanja_img : '',
                vrsta_korisnika : ''
            }
            this.provera = ''
            
           
            
            axios.post('http://127.0.0.1:5000/register',{
                username : this.korisnik.username,
                password : this.korisnik.password,
                confirm_password : this.korisnik.confirm_password,
                email : this.korisnik.email,
                godiste : this.korisnik.godiste,
                putanja_img : this.korisnik.putanja_img,
                stanje_novca : this.korisnik.stanje_novca,
                vrsta_korisnika : this.korisnik.vrsta_korisnika
            })
            .then((response) => {
                console.log('Odgovor sa servera:', response.data);
                this.$router.push({name:'login'});
                this.provera = '';
            })
            .catch((error) => {
                console.log(error);
                if (error.response && error.response.data && error.response.data.message) {
                    this.provera = error.response.data.message;
                } 
                else {
                    this.provera = "Došlo je do greške prilikom obrade zahtjeva.";
                }
            })

            
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