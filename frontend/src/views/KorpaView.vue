<template>
  <div v-if="proizvodi.length" class="container">
    <div class="main">
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th>Proizvod</th>
                <th colspan="2">Kolicina</th>
                <th>Cena</th>
                <th>Ukupna cena</th>
                <th>Opcija</th>
            </tr>
            <tr v-for="proizvod in proizvodi" :key="proizvod.id">
                <td>{{ proizvod.naziv }}</td>
                <td>
                    <div class="kolicina">
                        <button @click="smanjiJedan(proizvod)" class="btn btn-primary">-</button>
                        <p>{{ proizvod.kolicina }}</p>
                        <button  @click="povecajZaJedan(proizvod)" class="btn btn-primary">+</button>
                    </div>
                </td>
                <td><button @click="azurirajKolicinu(proizvod)" class="btn btn-primary">Update</button></td>
                <td>{{ proizvod.cena }}</td>
                <td>{{ proizvod.cena * proizvod.kolicina }}</td>
                <td><button @click="obrisiProizvod(proizvod.id)" class="btn btn-danger">Obrisi</button></td>
            </tr>            
        </table>
    </div>
    <div class="kupovina">
        <p>Za placanje: {{ izracunajUkupnuCenu(proizvodi) }}</p>
        <span>{{ greska }}</span>
        <button @click="naplatiProizvode()" class="btn btn-primary">Kupi</button>
    </div>
  </div>
  <div v-else class="novi">
    <h3>Trenutno nemate proizvode u korpi!</h3>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    props : ['korisnik_id'],
    data(){
        return {
            proizvodi : [],
            id_korisnika : '',
            greska : ''
        }
    },
    methods : {
        fechProducts(){
            axios.get(`http://127.0.0.1:5000/cart/${this.korisnik_id}`)
            .then((response) => {
                console.log(response);
                this.proizvodi = response.data.data.proizvodi;
            })
            .catch((error) => {
                console.log(error);
            })
        },
        obrisiProizvod(product_id){
            axios.delete(`http://127.0.0.1:5000/cart/delete/${product_id}`)
            .then((response) => {
                console.log(response);
                location.reload()
            })
            .catch((error) => {
                console.log(error);
            })
        },
        smanjiJedan(proizvod){
            if(proizvod.kolicina > 1){
                proizvod.kolicina--
            }
        },
        povecajZaJedan(proizvod){
            if(proizvod.kolicina < proizvod.kolicna_na_stanju){
                proizvod.kolicina++
            }
        },
        azurirajKolicinu(proizvod){
            axios.put(`http://127.0.0.1:5000/cart/update/${proizvod.id}`,{
                kolicina : proizvod.kolicina
            })
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.log(error);
            })
        },
        izracunajUkupnuCenu(proizvodi) {
            return proizvodi.reduce((ukupnaCena, proizvod) => {
                return ukupnaCena + (proizvod.cena * proizvod.kolicina);
            }, 0);
        },
        dohvatiID(){
            const stored_data = localStorage.getItem('id')
            if(stored_data){
                this.id_korisnika = JSON.parse(stored_data)
            }
        },
        naplatiProizvode(){
            const ukupnaCena = this.izracunajUkupnuCenu(this.proizvodi)
            axios.post(`http://127.0.0.1:5000/checkout`,{
                cena : ukupnaCena,
                korisnik_id : this.id_korisnika,
                proizvodi : this.proizvodi
            })
            .then((response) => {
                console.log(response);
                this.greska = ''
                this.$router.push({name:'proizvodi'})
            })
            .catch((error) => {
                console.log(error);
                this.greska = error.response.data.message;
            })
        }
    },
    mounted(){
        this.fechProducts()
        this.dohvatiID()
    },

    
}
</script>

<style scoped>
    table th,
    table td{
        padding: 1em;
        text-align: center;
    }
    .main{
        display: flex;
        justify-content: center;
        margin-top: 5em;
    }
    .kolicina{
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    .kupovina{
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-top: 2em;
        align-items: center;
        gap: 1em;
    }
    .kupovina p{
        font-weight: bold;
    }
    span{
        color: red;
    }
    .novi{
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .novi h3{
        font-size: 3em;
        color: red;
    }
</style>