<template>
  <div class="container">
    <h1>Svi korisnici</h1>  
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Password</th>
            <th>Email</th>
            <th>Godiste</th>
            <th>Stanje novca</th>
            <th>Tip korisnika</th>
            <th colspan="2">Opcije</th>
        </tr>
        <tr v-for="korisnik in svi_korisnici" :key="korisnik.id">
            <td>{{ korisnik.id }}</td>
            <td>{{ korisnik.username }}</td>
            <td>{{ korisnik.password }}</td>
            <td>{{ korisnik.email }}</td>
            <td>{{ korisnik.godiste }}</td>
            <td>{{ korisnik.trenutno_stanje_novca }}</td>
            <td>{{ korisnik.tip_korisnika }}</td>
            <td><router-link :to="`/admin/users/update/${korisnik.username}`" @click="azurirajKorisnika(korisnik.id)" class="btn btn-primary">Update</router-link></td>
            <td><button @click="obrisiKorisnika(korisnik.id)" class="btn btn-danger">Delete</button></td>
        </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    data(){
        return{
            svi_korisnici : []
        }
    },
    methods : {
        fetchAllUsers(){
            axios.get('http://127.0.0.1:5000/admin/users')
            .then((response)=> {
                console.log(response);
                this.svi_korisnici = response.data.data;
                console.log(this.svi_korisnici);
            })
            .catch((error) => {
                console.log(error);
            })
        },
        obrisiKorisnika(id){
            axios.delete(`http://127.0.0.1:5000/admin/users/delete/${id}`)
            .then((response) => {
                console.log(response);
                location.reload()
            })
            .catch((error) => {
                console.log(error);
            })
        }, 
    },
    mounted(){
        this.fetchAllUsers()
    }
}
</script>

<style scoped>
    table th,
    table td{
        padding: 1em;
        text-align: center;
    }
</style>