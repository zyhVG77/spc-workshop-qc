const state = () => ({
    sub_sys: "workshop"
})

const mutations = {
    changeSubSys: function(state, name) {
        state.sub_sys = name;
    }
}

const actions = {
    changeSubSys({commit, state}) {
        return new Promise(((resolve, reject) => {
            try {
                if (state.sub_sys === "workshop") {
                    commit("changeSubSys", "warehouse")
                    resolve('warehouse')
                }
                else {
                    commit("changeSubSys", "workshop")
                    resolve('workshop')
                }
            }
            catch(e) {
                reject()
            }
        }))
    }
}

const getters = {
    current_sub_sys: state => state.sub_sys
}


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}