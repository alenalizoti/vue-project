<template>
  <div class="container" v-if="chekIfLogged">
    <h2 class="title">Moji proizvodi</h2>
    <div class="novi">
      <button @click="dodajNovi" class="btn btn-primary">Dodaj novi</button>
    </div>
    <div class="proizvodi">
      <div class="proizvod col-md-3" v-for="proizvod in proizvodi" :key="proizvod.id">
          <img :src="`../../public/products/` + proizvod.naziv.split(' ')[0] + proizvod.image_extension" alt="">
          <h3 class="naziv">{{ proizvod.naziv }}</h3>
          <p class="opis">{{ sredi_description(proizvod.opis) }}</p>
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
              </div>
            </div>
            
          </div>
          <div class="opcije">
            <router-link :to="`/update_product/${proizvod.id}`" class="btn btn-primary" >Izmeni</router-link>
            <button @click="obrisi_proizvod(proizvod.id)" class="btn btn-danger">Obrisi</button>
            <router-link :to="`/proizvod/`+proizvod.id" class="btn btn-primary">Pogledaj proizvod</router-link>
          </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
export default {
    props : ['username'],
    data(){
        return{
            proizvodi : [],
            role : '',
            naziv_kafe : '',
        }
    },
    methods : {
        sendData(){
            axios.get(`http://127.0.0.1:5000/products/prodavac/${this.username}`,{
            })
            .then((response) => {
                console.log(response);
                this.proizvodi = response.data.data;
                console.log(this.proizvodi);
            })
            .catch((error) => {
                console.log(error);
            })
        },
        sredi_description(description) {
            const novi_description = description.slice(0, 97) + "...";
            return novi_description;
        },
        dohvatiRole(){
            const stored_data = localStorage.getItem('role')
            if (stored_data){
                this.role = JSON.parse(stored_data)
            }
        },
        izracunajCenu(cena,snizenje){
            cena = cena - (cena * (snizenje/100))
            return cena
        },
        dodajNovi(){
            this.$router.push({name:'add-new'})
        },
        brisi_proizvod(id){
            axios.delete(`http://127.0.0.1:5000/product/delete/${id}`)
            .then((response) => {
            console.log(response);
            this.$router.push({ name: 'prodavac' });
            location.reload();
            })
            .catch((error) => {
            console.log(error);
            })
        }
     
    },
    mounted(){
        this.sendData()
        this.dohvatiRole()
    },
    computed : {
        chekIfLogged(){
            const stored_data = localStorage.getItem('role')
            return !!stored_data
        }
    },
    
}
</script>

<style scoped>
  
  .proizvodi{
    display: flex;
    flex-wrap: wrap;
    gap: 3em;
  }
  .proizvod img{
    height: 15em;
    width: 15em; 
    border-radius: 5px;
  }
  .proizvod{
      color: #fff;
      background-color: rgba(139, 69, 19, 0.8);
      padding: 1em;
      display: flex;
      flex-direction: column;
      align-items: center;
      border-radius: 9px;
      width: 30%;
  }
  .naziv{
    text-align: center;
  }
  .opis{
    text-align: center;
  }
  .sredi_cenu_bez,
  .popust,
  .nova_cena{
    display: flex;
    align-items: center;
    gap: 1.5em;
  }
  .title{
    text-align: center;
  }
  .novi{
    display: flex;
    justify-content: center;
    margin: 2em 0;
  }
  .opcije{
    display: flex;
    gap: 2em;
  }
  .stara_cena{
    text-decoration: line-through;
  }
</style>