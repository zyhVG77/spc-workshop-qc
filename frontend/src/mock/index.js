import axios from 'axios'
import MockAdapter from "axios-mock-adapter"

export default {
    startMonk: function () {
        const mock = new MockAdapter(axios)
        mock.onPost("/api/user/ConfirmLogin").reply(config => {
            console.log(config.data)
            const response = {
                status: "success",
                token: "1"
            }
            return [200, JSON.stringify(response)]
        })
        mock.onGet('/api/user/GetUserInfo').reply(200, {
            status: "success",
            user: {
                id: "1",
                username: "test",
                email: "lucyinthesky@beatles.com",
                fullname: "11",
                workId: "11",
                avatar: "#",
                role: "admin"
            }
        })
        mock.onGet("/api/workshop/GetAllProducts").reply(200, {
            status: "success",
            products: [
                {id: "001",name:"产品1",type:"类型1",description:"描述1",
                    parameters: [
                        {id: "x001",name: "参数1",value_type: "variable_data", scale: "s1", unit: "u1", graph_type: "Xbar-s", usl: "u1", lsl: "l1", description: "d1", control_plan_id: "cp00001"},
                        {id: "x002",name: "参数2",value_type: "variable_data", scale: "s2", unit: "u2", graph_type: "Xbar-R", usl: "u2", lsl: "l2", description: "d2", control_plan_id: "cp00002"},
                        {id: "x003",name: "参数3",value_type: "variable_data", scale: "s3", unit: "u3", graph_type: "I-MR", usl: "u3", lsl: "l3", description: "d3", control_plan_id: "cp00003"},
                        {id: "x004",name: "参数4",value_type: "attribute_data", scale: "s4", unit: "u4", graph_type: "p", usl: "u3", lsl: "l3", description: "d3", control_plan_id: "cp00004"}],
                    workshop: [
                        {measure_plan_id: "mp000001", workshop_name: "车间1"},
                        {measure_plan_id: "mp000002", workshop_name: "车间2"},
                        {measure_plan_id: "mp000003", workshop_name: "车间3"},
                    ]
                },
                {id: "002",name:"产品2",type:"类型2",description:"描述2",
                    parameters: [
                        {id: "x101", name: "参数1",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x102", name: "参数2",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x103", name: "参数3",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""}],
                    workshop: [
                        {measure_plan_id: "mp000001", workshop_name: "车间4"},
                        {measure_plan_id: "mp000002", workshop_name: "车间5"},
                        {measure_plan_id: "mp000003", workshop_name: "车间6"},
                    ]
                },
                {id: "003",name:"产品3",type:"类型3",description:"描述3",
                    parameters: [
                        {id: "x201", name: "参数1",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x202", name: "参数2",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x203", name: "参数3",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""}],
                    workshop: [
                        {measure_plan_id: "mp000001", workshop_name: "车间1"},
                        {measure_plan_id: "mp000002", workshop_name: "车间2"},
                        {measure_plan_id: "mp000003", workshop_name: "车间3"},
                    ]
                },
                {id: "004",name:"产品5(无车间)",type:"类型3",description:"描述3",
                    parameters: [
                        {id: "x201", name: "参数1",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x202", name: "参数2",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x203", name: "参数3",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""}],
                    workshop: []
                }
            ]
        })
        mock.onPost('/api/workshop/SubmitProduct').reply(config => {
            console.log(config.data)
            return [200, {
                product: {id: "004",name:"产品4",type:"类型4",description:"描述4",
                    parameters: [
                        {id: "x201", name: "参数1",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x202", name: "参数2",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""},
                        {id: "x203", name: "参数3",value_type: "", scale: "", unit: "", graph_type: "", usl: "", lsl: "", description: ""}]
                },
                status: 'success'
            }]
        })
        mock.onGet('/api/workshop/DeleteProduct').reply(200, {
            status: 'success'
        })
        mock.onPost('/api/user/ModifyPassword').reply(200, {
            status: 'success'
        })
        mock.onPost('/api/user/UpdateUserInfo').reply(config => {
            console.log(config.data)
            return [200, {
                status: 'success',
                user: {
                    id: "2",
                    username: "test_2",
                    email: "fearless@pinkfloyd.com",
                    fullname: "ya",
                    workId: "000001",
                    avatar: "#"
                }
            }]
        })
        mock.onGet('/api/workshop/GetAllExceptionReports').reply(200, {
            status: 'success',
            reports: [
                {
                    id: "e000001",
                    product: "齿轮",
                    parameter: "内径",
                    measure_plan: "m000001",
                    measure_form_id: "p0000001",
                    time: "2021年2月23日",
                    information: "这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息",
                    read: false
                },
                {
                    id: "e000001",
                    product: "齿轮",
                    parameter: "内径",
                    measure_plan: "m000001",
                    measure_form_id: "p0000001",
                    time: "2021年2月23日",
                    information: "这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息",
                    read: false
                },
                {
                    id: "e000001",
                    product: "齿轮",
                    parameter: "内径",
                    measure_plan: "m000001",
                    measure_form_id: "p0000001",
                    time: "2021年2月23日",
                    information: "这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息",
                    read: false
                },
                {
                    id: "e000001",
                    product: "齿轮",
                    parameter: "内径",
                    measure_plan: "m000001",
                    measure_form_id: "p0000001",
                    time: "2021年2月23日",
                    information: "这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息",
                    read: true
                },
                {
                    id: "e000001",
                    product: "齿轮",
                    parameter: "内径",
                    measure_plan: "m000001",
                    measure_form_id: "p0000001",
                    time: "2021年2月23日",
                    information: "这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息",
                    read: true
                },
                {
                    id: "e000001",
                    product: "齿轮",
                    parameter: "内径",
                    measure_plan: "m000001",
                    measure_form_id: "p0000001",
                    time: "2021年2月23日",
                    information: "这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息这是异常信息",
                    read: true
                },
            ]
        })
        mock.onGet('/api/workshop/GetAllWorkshopsInfo').reply(200, {
            status: 'success',
            workshops: [
                {
                    id: '#001',
                    name: '车间001',
                    productId: '001',
                    batchSize: 20,
                    windowSize: 20,
                    description: 'a description'
                },
                {
                    id: '#002',
                    name: '车间002',
                    productId: '002',
                    batchSize: 20,
                    windowSize: 20,
                    description: 'a description'
                },
                {
                    id: '#003',
                    name: '车间003',
                    productId: '003',
                    batchSize: 20,
                    windowSize: 20,
                    description: 'a description'
                },
                {
                    id: '#004',
                    name: '车间003',
                    productId: '001',
                    batchSize: 20,
                    windowSize: 20,
                    description: 'a description'
                }
            ]
        })
    }
}
