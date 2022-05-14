import axios from 'axios'

export function testConnection(address) {
    return axios.post('/api/workshop/testUaConnection', { address })
}

export function connectUa(address) {
    return axios.post('/api/workshop/connectUa', { address })
}

export function fetchModel() {
    return axios.get('/api/workshop/fetchInformationModel')
}


// // 推荐写成这种格式（api文件中）
// export function submitProduct(product) {
//     return axios.post('/api/warehouse/submitProduct', { product } /* 或 { product: product } */)
// }
//
// // 在视图写（导入和调用）
// // 导入
// import { submitProduct } from '@/api/warehouse.js' /* api文件位置 */
// // 调用
// submitProduct(this.product /* 视图data里的数据 */)
//     .then(resp => {
//         resp = resp.data /* 这时resp就是后端返回的字典 */
//         /*
//             在这里处理后端返回的数据
//          */
//     })
//     .catch(err => {
//         /*
//             在这里处理错误
//          */
//     })
