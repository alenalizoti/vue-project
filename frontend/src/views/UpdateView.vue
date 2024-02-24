<template>
    <div class="parent">
        <form >
            <h2>Update {{ username }}</h2>
            {{ provera }}
            <p>
                <label>Username</label>
                <input type="text" v-model="user.username" readonly>
            </p>
            <p>
                <label>Password</label>
                <input type="password" v-model="password">
            </p>
            <p>
                <label>New password</label>
                <input type="password" v-model="new_password">
            </p>
            <p>
                <label>Email</label>
                <input type="email" v-model="user.email">
            </p>
            <p>
                <label>Godina rodjenja</label>
                <input type="number" v-model="user.godiste">
            </p>
            <p>
                <label>Profilna slika</label>
                <input class="image" type="file"  @change="handleFileChange" ref="image_file">
               
            </p>
            <p>
                <label>Trenutno stanje novca</label>
                <input type="text" readonly v-model="user.trenutno_stanje_novca">   
            </p>
            <p>
                <label>Vrsta korisnika</label>
                <input type="text" v-model="user.tip_korisnika" readonly>
            </p>

            <p>
                <button @click.prevent="updateKorisnika" class="btn btn-primary">Update</button>
                <button class="btn btn-danger"><router-link :to="`/profil/${username}`">Cancel</router-link></button>
            </p>
        </form>
    </div>
</template>


<script>
import axios from 'axios';
export default {
    props : ['username'],
    data(){
        return { 
            user : {},
            provera : "",
            new_password :'',
            password : '',
            putanja : ''
            
        }
    },
    mounted(){
        this.fetchUser()
    },
    methods: {
       fetchUser(){
            const username = this.username
            axios.get(`http://127.0.0.1:5000/profil/update/${username}`)
            .then((response) => {
                console.log(response);
                this.user = response.data.data;
            })
            .catch((error) => {
                console.log(error);
            })
       },
       handleFileChange(){
            const fileInput = this.$refs.image_file;
            var file = null
            if (fileInput.files.length > 0){
                file = fileInput.files[0]
            }
            const reader = new FileReader();
            reader.onloadend = () => {
                this.putanja = reader.result.split(',')[1]
            }

            reader.readAsDataURL(file)
        },
       updateKorisnika(){
            axios.put(`http://127.0.0.1:5000/profil/update/${this.username}`,{
                username : this.user.username,
                password : this.password,
                new_password : this.new_password,
                email : this.user.email,
                godiste : this.user.godiste,
                putanja_img : this.putanja
            })
            .then((response) => {
                console.log(response);
                this.provera = ''
                console.log(this.password);
                console.log(this.new_password);
                this.$router.push({name:'profil'})
            })
            .catch((error) => {
                console.log(error);
                this.provera = error.response.data.message;
                console.log(this.password);
                console.log(this.new_password);
                console.log(this.user.image_path);
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
        height: 110vh;
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