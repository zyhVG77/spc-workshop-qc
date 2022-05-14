import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'


Vue.use(VueAxios, axios)
Vue.config.productionTip = false

/*
  Add a request interceptor so that
  every request will be sent with token.
*/
axios.interceptors.request.use(function (config) {
  let token = localStorage.getItem("token")
  if (token) {
    config.headers.common["Authentication"] = token
  }
  return config
}, function (error) {
  return Promise.reject(error)
})

/*
  Register a Navigation Guard
  Handle Unauthorized Access Cases
*/
router.beforeEach((to, from, next) => {
    // If the token is in the LocalStorage
    if (store.getters['user/isLoggedIn']) {
        // Check whether the user info has been fetched
        const currentUser = store.getters['user/currentUser']
        if (!currentUser || !currentUser.role) {
            store.dispatch('user/getUserInfo')
                .then(user => {
                    // Generate router map
                    store.dispatch('permission/generateRoutes', user.role)
                        .then(() => {
                            router.addRoutes(store.getters["permission/customRoutes"])
                            // console.log(router.getRoutes())
                            next({...to, replace: true})
                        })
                })
                .catch(err => {
                    console.log(err)
                    store.dispatch('user/logout').then(() => {}).catch(() => {})
                    next('login')
                })
        } else {
            next()
        }
    } else if (to.fullPath === '/login') {
        next()
    } else {
        next('/login')
    }
})

/*
    Monk Response Data For testing
*/
// import monk from '@/mock/mock_warehouse'
// monk.startMonk()

/*
    Use VCalendar
 */
import VCalendar from 'v-calendar'
Vue.use(VCalendar);

import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'
Vue.use(VueToast)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
