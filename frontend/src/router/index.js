import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path : '/',
      component : () => import ('@/layout/Default.vue'),
      children : [
        {
          path: '/',
          name: 'home',
          component: HomeView
        },
        {
          path: '/proizvodi',
          name: 'proizvodi',
          component: () => import('../views/ProizvodiView.vue')
        },
        {
          path: '/profil/:username',
          name: 'profil',
          component: () => import('../views/ProfilView.vue'),
          props : true
        },
        {
          path: '/update/:username',
          name: 'update',
          component: () => import('../views/UpdateView.vue'),
          props : true
        },
        {
          path: '/novi',
          name: 'add-new',
          component: () => import('../views/NoviProizvodView.vue')
        },
        {
          path: '/update_product/:id',
          name: 'update_product',
          component: () => import('../views/UpdateProizvodView.vue'),
          props : true
        },
        {
          path: '/prodavac/:username',
          name: 'prodavac',
          component: () => import('../views/ProdavacView.vue'),
          props : true
        },
        {
          path: '/proizvod/:id',
          name: 'proizvod_opsirno',
          component: () => import('../views/ProizvodView.vue'),
          props : true
        },
        {
          path: '/cart/:korisnik_id',
          name: 'korpa',
          component: () => import('../views/KorpaView.vue'),
          props : true
        },
        {
          path: '/admin//users',
          name: 'all_users',
          component: () => import('../views/SviKorisnici.vue'),
        },
        {
          path: '/admin/users/update/:username',
          name: 'admin-update',
          component: () => import('../views/AdminUpdateUsersView.vue'),
          props : true
        },
      ]
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },

  ]
})

export default router
