import {constantRouterMap, asyncRouterMap} from "@/router/index";

function hasPermission(role, route) {
    if (route.meta && route.meta.role)
        return route.meta.role.indexOf(role) >= 0
    else
        return true
}

const state = () => ({
    routes: constantRouterMap,
    customRoutes: []
})

const mutations = {
    setRoutes(state, routes) {
        state.customRoutes = routes
        state.routes = constantRouterMap.concat(routes)
    }
}

const actions = {
    generateRoutes({commit}, role) {
        return new Promise(resolve => {
            // The children routes has been considered
            const accessRoute = asyncRouterMap.filter(v => {
                if (hasPermission(role, v)) {
                    if (v.children && v.children.length > 0) {
                        // Check every children route
                        // Pick the routes to which the user has permission
                        v.children = v.children.filter(child => {
                            if (hasPermission(role, child)) {
                                return child
                            }
                            return false
                        })
                    }
                    return v
                } else {
                    return false
                }
            })
            commit('setRoutes', accessRoute)
            resolve()
        })
    }
}

const getters = {
    routes: state => state.routes,
    customRoutes: state => state.customRoutes
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}