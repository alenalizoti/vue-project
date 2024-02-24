<template>
    <div class="parent">
        
        <form>
            <h1>Izmenite prozivod</h1>
            {{ greska }}
            <p>
                <label>Unesite naziv</label>
                <input type="text" v-model="proizvod.naziv" readonly>
            </p>
            <p>
                <label>Unesite opis</label>
                <input type="textarea" v-model="proizvod.opis">
            </p>
            <p>
                <label>Unesite cenu</label>
                <input type="number" v-model="proizvod.cena">
            </p>
            <p>
                <label>Unesite kolicinu na stanju</label>
                <input type="number" v-model="proizvod.kolicna_na_stanju">
            </p>
            <p>
                <label>Popust</label>
                <input type="number" v-model="proizvod.opcija_za_snizenje">
            </p>
            <p>
                <button @click.prevent="updateProduct" class="btn btn-primary">Izmeni</button>
                <button class="btn btn-danger"><router-link :to="`/prodavac/${username}`">Cancel</router-link></button>
            </p>
        </form>
    </div>
    
</template>

<script>
import axios from 'axios'
export default {
    props : ['id'],
    data(){
        return{
            proizvod : {},
            greska : '',
            role : '',
            username : ''
        }
    },
    methods : {
        fetchProduct(){
            const id_proizvoda = this.id
            axios.get(`http://127.0.0.1:5000/update_product/${id_proizvoda}`)
            .then((response) => {
                console.log(response);
                this.proizvod = response.data.data;
                console.log(this.proizvod);
            })
            .catch((error) => {
                console.log(error);
            })
        },
        updateProduct(){
            const id_proizvoda = this.id
            axios.put(`http://127.0.0.1:5000/update_product/${id_proizvoda}`,{
                naziv : this.proizvod.naziv,
                opis : this.proizvod.opis,
                cena : this.proizvod.cena,
                kolicina : this.proizvod.kolicna_na_stanju,
                popust : this.proizvod.opcija_za_snizenje
            })
            .then((response) =>{
                this.greska = '';
                this.$router.push({ path : `/prodavac/${this.username}` });
            })
            .catch((error) => {
                console.log(error);
                this.greska = error.response.data.message;
            })
        },
        dohvatiUsername(){
            const stored_data = localStorage.getItem('username')
            if(stored_data){
                this.username = JSON.parse(stored_data)
            }
        }
    },
    mounted(){
        this.fetchProduct()
        this.dohvatiUsername()
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