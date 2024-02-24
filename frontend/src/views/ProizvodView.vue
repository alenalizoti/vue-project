<template>
    <div class="container">
        <div class="main">
            <div class="proizvod-slika">
                <!-- <img :src="`../../public/products/${proizvod.naziv.split(' ')[0]}${proizvod.image_extension}`" alt=""> -->
                <img v-if="proizvod.naziv && proizvod.image_extension" :src="`../../public/products/${proizvod.naziv.split(' ')[0]}${proizvod.image_extension}`" alt="">
            </div>
            <div class="about">
                <div class="about-product">
                    <h2>{{ proizvod.naziv }}</h2>
                    <p>{{ proizvod.opis }}</p>
                </div>
                <div class="cena">
                    <div class="sredi_cenu_bez" v-if="(proizvod.cena * proizvod.opcija_za_snizenje) == proizvod.cena">
                        <p>{{ proizvod.cena }} RSD</p>
                        <p>Na stanju: {{ proizvod.kolicna_na_stanju }}</p>
                    </div>
                
                    <div v-else>
                    <div class="popust">
                            <p>Popust: {{ proizvod.opcija_za_snizenje }} %</p>
                            <p class="stara_cena">{{ proizvod.cena }} RSD</p>
                    </div>
                    <div class="nova_cena">
                            <p>Cena: {{ izracunajCenu(proizvod.cena,proizvod.opcija_za_snizenje) }}</p>
                            <p>Na stanju: {{ proizvod.kolicna_na_stanju }}</p>
                            <span>{{ greska_kolicina }}</span>
                    </div>
                </div>
                <div v-if="role == 'kupac'" class="porudzbina">
                    <button :disabled="proveriBrojProizvoda" @click="smanjiJedan" class="btn btn-primary">Smanji</button>
                    <p>{{ broj_proizvoda }}</p>
                    <button :disabled="proveriBroj" @click="povecajZaJedan" class="btn btn-primary">Dodaj</button>
                </div>
                <span>{{ greska_kolicina }}</span>
                <div v-if="role =='kupac'" class="korpa">
                    <p>{{ message }}</p>
                    <button @click="addInCart" class="btn btn-primary">Dodaj u korpu</button>
                </div>
            </div>  
        </div>
        
    </div>
    <div class="komentari">
        <div v-if="role == 'kupac'" class="unos-komentara">
            <h1>Dodajte komentar</h1>
            <span class="greska">{{ greska }}</span>
            <div class="input">
                <input type="text" class="form-control unos" placeholder="Unesite komentar" v-model="komentar">
            </div>
            <div class="dugme_slanje">
                <button @click="posaljiKomentar" class="btn btn-primary">Postavi</button>
            </div>
        </div>
        <div v-else-if="role == 'admin' || role == 'prodavac'" class="izmena_komentara">
            
            <div v-if="svi_komentari.length" class="svi_komentari">
                <h1 >Uredite komentare</h1>
                <div v-for="komentar in svi_komentari" :key="komentar.id" class="komentar">
                    <div class="gore">
                        <p class="name">{{ komentar.username }}</p>
                        <p>{{ komentar.datum_komentarisanja }}</p>
                    </div>
                    <div class="sadrzaj">
                        {{ komentar.sadrzaj }}
                    </div>
                    <div class="obrisi">
                        <button @click="obrisi_komentar(komentar.id)" class="btn btn-danger">Obirisi</button>
                    </div>
                </div>
            </div>
            <div v-else class="div">
                <h1>Nema komentara</h1>
            </div>
        </div>
        
    </div>
  </div>
  
</template>

<script>
import axios from 'axios'
export default {
    props : ['id'],
    data(){
        return {
            proizvod : {},
            broj_proizvoda : 1,
            role : '',
            komentar : '',
            greska : '',
            id_korisnika : '',
            svi_komentari : [],
            greska_kolicina : '',
            message : '',
            greska_kolicina : ''
        }
    },
    methods : {
        fetchProduct(){
            const id = this.id
            axios.get(`http://127.0.0.1:5000/product/${id}`)
            .then((response) => {
                console.log(response);
                this.proizvod = response.data.data;
                console.log(this.proizvod);
                console.log(this.proizvod.naziv);
                this.dohvati_komentare()
            })
            .catch((error) =>{
                console.log(error);
            })
        },
        izracunajCenu(cena,snizenje){
            cena = cena - (cena * (snizenje/100))
            cena = parseFloat(cena.toFixed(2));
            return cena
        },
        smanjiJedan(){
            if(this.broj_proizvoda > 1){
                this.broj_proizvoda--
            }
        },
        povecajZaJedan(){
            if(this.broj_proizvoda < this.proizvod.kolicna_na_stanju){
                this.broj_proizvoda++
            }
        },
        dohvatiRole(){
            const stored_data = localStorage.getItem('role')
            if(stored_data){
                this.role = JSON.parse(stored_data)
                console.log(this.role);
            }
        },
        posaljiKomentar(){
            axios.post(`http://127.0.0.1:5000/products/${this.id}/comment`,{
                komentar : this.komentar,
                id_korisnika : this.id_korisnika
            })
            .then((response) => {
                console.log(response);
                this.greska = '';
                this.komentar = '';
            })
            .catch((error) => {
                console.log(error);
                this.greska = error.response.data.message;
            })
        },
        idKorisnika(){
            const stored_data = localStorage.getItem('id')
            if(stored_data){
                this.id_korisnika = JSON.parse(stored_data)
            }
        },
        dohvati_komentare(){
            axios.get(`http://127.0.0.1:5000/products/comments/${this.id}`)
            .then((response) => {
                console.log(response);
                this.svi_komentari = response.data.data;
            })
            .catch((error) => {
                console.log(error);
            })
        },
        obrisi_komentar(komentar_id){
            axios.delete(`http://127.0.0.1:5000/products/${this.id}/comment/delete/${komentar_id}`)
            .then((response) => {
                console.log(response);
                location.reload();
            })
            .catch((error) => {
                console.log(error);
            })
        },
        addInCart(){
            axios.post(`http://127.0.0.1:5000/cart/add/${this.id}}`,{
                kolicina : this.broj_proizvoda,
                korisnik_id : this.id_korisnika
            })
            .then((response) => {
                console.log(response);
                this.message = 'Uspesno ste dodali proizvod u korpu!'
            })
            .catch((error) => {
                console.log(error);
                this.greska_kolicina = error.response.data.message;
            })
        }
    },
    mounted(){
        this.fetchProduct()
        this.dohvatiRole()
        this.idKorisnika()
    },
    computed : {
        proveriBrojProizvoda(){
            if(this.broj_proizvoda > 1){
                return false
            }
            return true
        },
        proveriBroj(){
            if(this.broj_proizvoda < this.proizvod.kolicna_na_stanju){
                return false
            }
            return true
        }
    }
}
</script>

<style scoped>
    .obrisi{
        display: flex;
        justify-content: center;
    }
    .gore{
        display: flex;
        justify-content: space-between;
    }
    .proizvod-slika img{
        width: 80%;
    }
    .name{
        font-weight: bold;
    }
    .greska{
        display: block;
        text-align: center;
        margin: 1em 0;
    }
    .main{
        display: flex;
        /* align-items: center; */
        justify-content: space-around;
        padding-top: 7em;
    }
    .main > div{
        width: 50%;
    }
    .about h2{
        text-align: center;
        font-size: 3em;
        margin-bottom: 1em;
    }
    .about p {
        font-size: 1.3em;
        text-align: center;
    }
    .about{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3em;
    }
    .sredi_cenu_bez,
    .popust,
    .nova_cena{
        display: flex;
        align-items: center;
        gap: 1.5em;
    }
    .stara_cena{
        text-decoration: line-through;
    }
    .porudzbina{
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        margin-top: 5em;
    }
    .korpa{
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-top: 2em;
    }
    .komentari h1{
        text-align: center;
        margin-top: 2em;
    }
    .input{
        display: flex;
        justify-content: center;
    }
    .unos{
        height: 5em;
        width: 70%;
    }
   .dugme_slanje{
        display: flex;
        justify-content: center;
        margin-top: 1em;
   }
   .svi_komentari{
        display: flex;
        flex-direction: column;
        gap: 1em;
        align-items: center;
   }
   .komentar{
    width: 60%;
    background-color: aqua;
    padding: 0.5em;
    border-radius: 5px;
   }
</style>