# API—质量控制

## 质量控制API

### 1 get control graph

**请求地址**：/api/warehouse/getControlGraph

**请求方式**：POST

**说明**：获取控制图

**输入**：  

```json
{
    measurePlanId: '',	// 测量计划id
    parameterId: '',	// 参数id
    start_time: '',	// 开始时间
    end_time: '',	// 结束时间
    // 注：不指明时间(start_time与end_time都为'')的情况下
    //     控制图的范围为所有记录
    analyze: true | false
}
```

**输出**：

```json
// 操作成功 && analyze为false
{
    status: 'success',
    option: obj	// option of e-charts
}
// 操作成功 && analyze为true
{
    status: 'success',
    html: obj	// html of the analysis
}
//操作失败
{
    status: 'fail',
    errorMsg: 'reason'
}
```

