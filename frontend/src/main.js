import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import '@/assets/css/main.css'
import '@/assets/fonts/style.css'

Vue.use(VueAxios, axios);
Vue.config.productionTip = false;

/*
  Add a request interceptor so that
  every request will be sent with token.
*/
axios.interceptors.request.use(function (config) {
  let token = localStorage.getItem("token");
  if (token) {
    config.headers.common["Authentication"] = token;
  }
  return config;
}, function (error) {
  return Promise.reject(error);
});

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
                .catch(err => console.log(err))
        } else {
            next()
        }
    } else if (to.fullPath === '/login') {
        next()
    } else {
        // next('/login')
        next()
    }
})

/*
    Monk Response Data For testing
*/
// import monk from '@/mock/index'
// monk.startMonk()

/*
    Use VCalendar
 */
import VCalendar from 'v-calendar'
Vue.use(VCalendar);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
