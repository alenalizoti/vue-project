<template>
  
    <div class=" parent">
        <form>
            <h2>Novi proizvod</h2>
            {{ greska }}
            <p>
                <label>Unesite naziv</label>
                <input type="text" v-model="proizvod.naziv">
            </p>
            <p>
                <label>Unesite opis</label>
                <input type="textarea" v-model="proizvod.opis">
            </p>
            <p>
                <label>Slika proizvoda</label>
                <input class="image" type="file" @change="handleFileChange" ref="image_file">
            </p>
            <p>
                <label>Unesite cenu</label>
                <input type="number" v-model="proizvod.cena">
            </p>
            <p>
                <label>Unesite kolicinu na stanju</label>
                <input type="number" v-model="proizvod.kolicina">
            </p>
            <p>
                <label>Popust</label>
                <input type="number" v-model="proizvod.popust">
            </p>
            <p>
                <button @click.prevent="dodajProizvod" class="btn btn-primary">Dodaj</button>
                <button class="btn btn-danger"><router-link :to="`/prodavac/${username}`" >Cancel</router-link></button>
            </p>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data(){
        return{
            proizvod : {
                naziv : '',
                opis : '',
                putanja_img : '',
                cena : '',
                kolicina : '',
                popust : 1
            },
            greska : '',
            username : ''
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
                this.proizvod.putanja_img = reader.result.split(',')[1]
            }

            reader.readAsDataURL(file)
        },
        dodajProizvod(){
            axios.post('http://127.0.0.1:5000/products/add',{
                naziv : this.proizvod.naziv,
                opis : this.proizvod.opis,
                putanja_img : this.proizvod.putanja_img,
                cena : this.proizvod.cena,
                kolicina : this.proizvod.kolicina,
                popust: this.proizvod.popust,
                username : this.username
            })
            .then((response) => {
                console.log(response);
                this.$router.push({path:`/prodavac/${this.username}`})
                this.greska = '';
            })
            .catch((error) => {
                console.log(error);
                this.greska = error.response.data.message;
            });
        },
        dohvatiUsername(){
            const stored_data = localStorage.getItem('username')
            if(stored_data){
                this.username = JSON.parse(stored_data)
                console.log(this.username);
            }
        }
        
    },
    mounted(){
        this.dohvatiUsername()
    }
    
}
</script>

<style scoped>
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