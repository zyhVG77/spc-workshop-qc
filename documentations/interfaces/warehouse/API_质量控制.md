# API——质量控制

### 1 Get control graph

**请求地址**：/api/warehosue/getControlGraph

**说明**：根据控制计划id获取控制图

**请求方式**：GET

**输入**：

```json
{
    controlPlanId: 'id of the control plan'
}
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    option: 'option of e-charts'
}
// 请求失败
{
    status: 'fail',
    errorMsg: 'reason'
}
```

### 2 Get exception report

**请求地址**：/api/warehouse/getExceptionReport

**说明**：根据控制计划id获取异常报告

**请求方式**：GET

**输入**：

```json
{
    controlPlanId: 'id of the control plan'
}
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    html: 'html of the exception page -> obj'
}
// 请求失败
// ...
```

