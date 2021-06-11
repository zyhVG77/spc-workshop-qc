import Vue from 'vue';
import Vuex from 'vuex';
// M#1 import createPersistedState from "vuex-persistedstate";

import user from './modules/user'
import products from "./modules/products";
import exceptions from "./modules/exceptions";
import permission from "./modules/permission";
import subsystem_state from "./modules/subsystem_state";
import warehouse_products from "./modules/warehouse_products";

Vue.use(Vuex)


/*
Modification: M#1 at 2021/2/26
- Detail: Remove the persistent plugin for user module
- Reason: if user information is NULL, the router guard
          will request the backend for it once again
 */

/* M#1

// Register a Plugin Instance for User Module
const userState = new createPersistedState({
    paths: ['user.user'],
    storage: window.sessionStorage
})

*/

const store = new Vuex.Store({
    modules: {
        user,
        products,
        exceptions,
        permission,
        subsystem_state,
        warehouse_products
    },
    // M#1 plugins: [userState],
})

export default store;