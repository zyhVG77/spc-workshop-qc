# API—测量计划管理

## 测量计划管理API

### 1 Submit Measure Plan

**请求地址**：/api/warehouse/SubmitMeasurePlan

**请求方式**：POST

**说明**：提交一个新的测量计划

**输入**：  

```json
{
    batchSize: 10, // 批容量
    batch: 10, // 批数
    productId: 'id of product', // 产品ID
    warehouseId: 'id of warehouse', // 仓库ID
    storageCellId: 'id of storage cell' // 储位ID
    description: 'description' // 批注
}
```

**输出**：  

```json
// 成功
{
    status: 'success'
}
// 失败
{
    status: 'fail',
    errorMsg: ''
}
```

### 2 Get Measure Plans

**请求地址**：/api/warehouse/GetMeasurePlans

**请求方式**：GET

**说明**：获取所有测量计划

**输入**：

```json
{}
```

**输出**：

```json
// 成功
{
    status: 'success',
    measurePlans: [
        {
            id: 'id of the measure plan', // 测量计划id
            storageCellId: '',	// 储位id
            batchSize: null,	// 批容量
            batch: null,	// 批数
            warehouse: {	// 仓库信息，应至少包含仓库id和仓库名
                id: '',
                name: ''
            },
            product: {		// 产品信息，应至少包含产品id和产品名
                id: '',
                name: '',
                parameters: [
                    {		// 参数列表，每个参数需包括如下控制信息
                		id: '',
                		name: '',
                    	unit: '',	// 单位
                    	scale: '',	// 小数位数
                    	graph_type: '',	// 控制图类型
                    	usl: '',	// 上规格限
                    	lsl: ''		// 下规格限
            		},
                    {
                        // ...
                    },
                    // ...
                ]
            }
        },
        {
            // ...
        },
        // ...
    ]
}
// 失败
// ...
```
<span style='color: red; font-weight: bold'>注意：管理员能获取所有测量计划</span>

### 3 Delete Measure Plan

**请求地址**：/api/warehouse/DeleteMeasurePlan

**请求方式**：GET

**说明**：删除一个测量计划

**输入**：

```json
{
    id: 'id of the measure plan'
}
```

**输出**：

```json
// 请求成功
{
    status: 'success'
}
// 请求失败
// ...
```
