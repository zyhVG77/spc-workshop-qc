import axios from 'axios'

const UserApi = {
    // Confirm Username and Password
    confirmLogin: function(user, success, fail, error) {
        axios.post('/api/user/ConfirmLogin', user)
            .then(resp => {
                const status = resp.data.status
                if (status === 'success')
                    success(resp.data.token)
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    // Get User Info
    getUserInfo: function(success, fail, error) {
        axios.get('api/user/GetUserInfo')
            .then(resp => {
                const status = resp.data.status
                if (status === 'success')
                    success(resp.data.user)
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => error('请求失败！'))
    },
    // Update User Info
    updateUserInfo: function (user, success, fail, error) {
        axios.post('/api/user/UpdateUserInfo', user)
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.user)
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    // Modify Password
    modifyPwd: function (data, success, fail, error) {
        axios.post('/api/user/ModifyPassword', data)
            .then(resp => {
                if (resp.data.status === 'success')
                    success()
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    //Get all existed users' id
    getUserId: function (success,fail,error) {
        axios.get('/api/user/getUserId')
            .then(resp => {
                if (resp.data.status === 'success')
                    success(resp.data.userid)
                else
                    fail(resp.data.errorMsg)
            })
            .catch(() => {
                error('请求失败！')
            })
    },
    //Submit the information of the user
    submitRelatonship: function (data) {
        axios.post('/api/user/submitRelatonship',data)
            .then(resp => {
                if (resp.data.status === 'success')
                    console.log(resp);
            })
            .catch(err => {
                console.log(err.data.errorMsg);
            })
    }
}

export default UserApi