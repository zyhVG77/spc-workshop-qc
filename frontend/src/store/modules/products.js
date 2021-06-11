import WorkshopApi from "@/api/workshop"

const state = () => ({
    status: '',
    all: []
})

const mutations = {
    loading: function (state) {
        state.status = 'loading'
    },
    loadFail: function (state) {
        state.status = 'fail'
    },
    setProducts: function(state, products) {
        state.status = 'loaded'
        state.all = products
    },
    addProduct: function(state, product) {
        state.all.push(product)
    },
    deleteProduct: function(state, index) {
        state.all.splice(index, 1)
    },
    modifyProduct: function(state, payload) {
        state.all[payload.index] = payload.product
        let tmp = state.all
        state.all = []
        state.all = tmp
    }
}

const actions = {
    getAllProducts: function ({ commit }) {
        return new Promise((resolve, reject) => {
            commit('loading')
            WorkshopApi.getAllProducts(
                (products) => {
                    commit('setProducts', products)
                    resolve(products)
                },
                (errorMsg) => reject(errorMsg),
                (errorMsg) => reject(errorMsg)
            )
        })
    },
    submitProduct: function({ commit }, payload) {
        const productForm = payload.productForm
        const modification = payload.modification

        return new Promise((resolve, reject) => {
            commit('loading')
            WorkshopApi.submitProduct(productForm, modification.modify,
                (product) => {
                    if (modification.modify) {
                        commit('modifyProduct', {index: modification.index, product})
                        resolve('修改成功！')
                    }
                    else {
                        commit('addProduct', product)
                        resolve('添加成功！')
                    }
                },
                (errorMsg) => {
                    reject(errorMsg)
                },
                (errorMsg) => {
                    commit('loadFail')
                    reject(errorMsg)
                })
        })
    },
    deleteProduct: function({ commit, state }, index) {
        return new Promise((resolve, reject) => {
            WorkshopApi.deleteProduct(state.all[index].id,
                () => {
                    commit('deleteProduct', index)
                    resolve()
                },
                (err) => reject(err),
                (err) => reject(err)
            )
        })
    }
}

const getters = {
    allProducts: state => state.all,
    loadStatus: state => state.status
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}