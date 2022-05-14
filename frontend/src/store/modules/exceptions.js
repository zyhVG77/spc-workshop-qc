import WorkshopApi from "@/api/workshop"

const state = () => ({
    status: '',
    all: [],
})

const mutations = {
    loading: function (state) {
        state.status = 'loading'
    },
    loadFail: function (state) {
        state.status = 'fail'
    },
    setReports: function (state, reports) {
        state.status = 'loaded'
        state.all = reports
    },
    markReportAsRead: function (state, index) {
        // When the reports has already been read
        // Skip it
        if (state.all[index].read)
            return

        // Otherwise, mark it as read
        // Using an Algorithm whose Time Complexity is O(n)
        const arr = state.all
        let i = index
        let tmp = arr[i]
        for (; i < arr.length - 1; ++i) {
            if (!arr[i+1].read)
                arr[i] = arr[i+1]
            else
                break
        }
        tmp.read = true
        arr[i] = tmp

        // Necessary for triggering the auto-update
        // in related Components
        state.all = null
        state.all = arr
    },
    deleteReport: function (state, idx) {
        state.all.splice(idx, 1)
    }
}

const actions = {
    getAllExceptionReports: function({commit}) {
        return new Promise( (resolve, reject) => {
            WorkshopApi.getAllExceptionReports(
                reports => {
                    commit('setReports', reports)
                    resolve()
                },
                err => reject(err),
                err => reject(err)
            )
        })
    },
    getReportDetailHtml: function({commit}, payload) {
        return new Promise((resolve, reject) => {
            WorkshopApi.getReportDetailHtml(payload.id,
                html => {
                    commit('markReportAsRead', payload.index)
                    // Convey the html string to front
                    resolve(html)
                },
                errorMsg => reject(errorMsg),
                errorMsg => reject(errorMsg)
            )
        })
    },
    deleteReport: function ({commit, state}, idx) {
        return new Promise((resolve, reject) => {
            WorkshopApi.deleteReport(state.all[idx].id)
                .then(resp => {
                    resp = resp.data
                    if (resp.status === 'success') {
                        commit('deleteReport', idx)
                        resolve()
                    }
                    else
                        reject(resp.errorMsg)
                })
                .catch(err => reject(err))
        })
    }
}

const getters = {
    reports: state => state.all,
    hasReport: state => state.all.length > 0,
    numberOfUnreadReports: state => {
        // Find the Index of Unread reports
        // Using Binary Search. Time Complexity: O(log n)
        const arr = state.all
        if (arr.length === 0)
            return 0
        let low = 0, high = arr.length - 1
        while (high - low > 1) {
            let mid = low + Math.floor((high - low) / 2)
            if (arr[mid].read)
                high = mid
            else
                low = mid
        }
        if (arr[low].read)
            return low
        return (arr[high].read) ? low + 1 : high + 1
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}