import { connectUa, fetchModel } from "@/api/opc-ua-api";

const state = () => ({
    uaAddress: '',
    connected: false,
})

const mutations = {
    setUaAddress: function(state, address) {
        state.uaAddress = address
    },
    setConnected: function(state) {
        state.connected = true
    }
}

const actions = {
    connectUaServer({commit}, address) {
        return new Promise(((resolve, reject) => {
            connectUa(address)
                .then(resp => {
                    if (resp.data.ok) {
                        commit('setUaAddress', address)
                        commit('setConnected')
                    } else {
                        throw new Error('连接失败！')
                    }
                    resolve()
                })
                .catch(err => { reject(err) })
        }))
    },
    fetchInfoModel({state}) {
        return new Promise((resolve, reject) => {
            if (state.connected) {
                fetchModel()
                    .then(resp => {
                        if (resp.data.status === 'success') {
                            resolve(resp.data.model)
                        } else {
                            reject(resp.data.errorMsg)
                        }
                    })
                    .catch(err => { reject(err) })
            } else {
                reject(new Error('服务器未连接！'))
            }
        })
    }
}

const getters = {
    uaAddress: state => state.uaAddress,
    uaConnected: state => state.connected,
}


export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
