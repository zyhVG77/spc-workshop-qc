import axios from 'axios'
const PutInFormApi = {
    submitPutInForm: function (data) {
        axios.post('/api/putinform/submitPutInForm',data)
         .then(resp => {
              if (resp.data.status === 'success')
                  console.log(resp);
         })
         .catch(err => {
         console.log(err.data.errorMsg);
         })
    }
}
export default PutInFormApi