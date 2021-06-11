# API—测量控制计划管理

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
    productId: 'id of the product', // 产品ID
    warehouseId: 'id of the warehouse', // 仓库ID
    parameters: ['id00001', 'id00002', '...'], // 测量属性ID的列表
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
            id: 'id of the measure plan',
            // ... 有待商议
            warehouseName: '',
            productName: ''
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

## 控制计划管理API

### 1 Submit Control Plan

**请求地址**：/api/warehouse/SubmitControlPlan

**说明**：提交控制计划

**请求方式**：POST

**输入**：

```json
{
    measurePlanId: 'measure plan id',	// 测量计划ID
    parameterId: 'parameter id',	// 控制属性ID
    description: 'description'	// 描述
}
```

**输出**：

```json
// 成功
{
    status: 'success'
}
// 失败
// ...
```

### 2 Get Control Plans

**请求地址**：/api/warehouse/GetControlPlans

**说明**：获取所有控制计划

**请求方式**：GET

**输入**：

```json
{}
```

**输出**：

```json
// 成功
{
	status: 'success',
    controlPlans: [
        {
            id: 'id of the control plan',	// 控制计划ID
            measurePlanId: 'id of the measure plan',	// 所属的测量计划ID
            warehouseName: '',	// 仓库名
            productName: '',	// 产品名
            batchSize: '',	// 批容量
            batch: '',	// 批数
            parameterName: ''	// 控制属性的名称
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

<span style='color: red; font-weight: bold'>注意：管理员能获取所有控制计划</span>

### 3 Delete Control Plan

**请求地址**：/api/warehouse/DeleteControlPlan

**说明**：删除一个测量计划

**请求方式**：GET

**输入**：

```json
{
    id: 'id of the control plan'	// 控制计划ID
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

