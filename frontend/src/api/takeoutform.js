import axios from 'axios'
const TakeOutFormApi = {
    submitTakeOutForm: function (data) {
        axios.post('/api/warehouse/submitTakeOutForm',data)
         .then(resp => {
              if (resp.data.status === 'success')
                  console.log(resp);
         })
         .catch(err => {
         console.log(err.data.errorMsg);
         })
    }
}
export default TakeOutFormApi