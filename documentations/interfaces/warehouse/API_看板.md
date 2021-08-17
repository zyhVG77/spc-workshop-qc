# API—看板

### 1 Get Warehouse Basic Info

**请求地址**：/api/warehouse/GetWarehouseBasicInfo

**说明**：获取看板上的信息

**请求方式**：GET

**输入**：

```json
{
    period: 'period time of statistics'
    // 共有5个取值
    // 1. today 今天
    // 2. 7days 近7天
    // 3. 15days 近15天
    // 4. 30days 近30天
    // 5. 1year 近1年
}
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    basicInfo: {
        'storeBatches': 10,  // 入库批数
        'storeAmount': 10,  // 入库数量
        'storeMoney': 10,  // 入库金额
        'deliverBatches': 10,  // 出库批数
        'deliverAmount': 10,  // 出库数量
        'deliverMoney': 10  // 出库金额
    },
    storeDeliverGraphOpiton: obj， // 出入库数量变化图的option
    occupationStateGraphOption: obj // 仓库占用状态图的option
}
// 请求失败
{
    status: 'fail',
 	errorMsg: 'reason or something else'
}
```

### 2 Get Warehouse Affairs

**请求地址**：/api/warehouse/GetWarehouseAffairs

**说明**：获取仓库最新的事件

**请求方式**：GET

**输入**：

```json
{}	// 注意这里并不提供仓库编号，因为人员与仓库是一对一的（总管对应所有仓库）
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    affairs: [
        {
            time: "The time when the event occurred",  // 事件发生的时间
            type: "sotre | deliver",  // 事件类型
            // 只有两个取值1. store代表入库 2. deliver代表出库
            detail: "detail of the event"  // 事件的详情
            // 形式：[入库|出库] $零件 $型号 * $数量 个 总价 $价格 元
            // 如：入库前照灯A101 * 200个 总价20000元
            operator: "operator of the event"  // 事件的操作员
        },
        {
            // ...
        }
        // ...
    ]
}
// 请求失败
// ...
```



# 2021年8月17日新增

### 3 Get Today Statistics

**请求地址**：/api/warehouse/GetTodayStatistics

**说明**：获取今日的统计数据

**请求方式**：GET

**输入**：

```json
{}    // 注意这里并不提供仓库编号，因为人员与仓库是一对一的（总管对应所有仓库）
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    statistics: {
        putInData: [    // 今日入库的产品-数量关系
        	['产品名', 数量],    // 注意：数量按从小到大的次序排列
        	['产品名', 数量],
    		// ......
        ],
        shippingData: [    // 今日出库的产品-数量关系
            ['产品名', 数量],    // 注意：数量按从小到大的次序排列
        	['产品名', 数量],
    		// ......
        ]
    }
}
// 请求失败
// ...
```

### 4 Get Full Year Statistics

**请求地址**：/api/warehouse/GetFullYearStatistics

**说明**：获取**过去**12个月的统计数据

**请求方式**：GET

**输入**：

```json
{}    // 注意这里并不提供仓库编号，因为人员与仓库是一对一的（总管对应所有仓库）
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    statistics: {
        putInData: {    // 过去12个月的入库数据
            月份: [第1天的入库量, 第2天的入库量, ......],
            月份: [第1天的入库量, 第2天的入库量, ......],
            // 共计12个月
            // 【注意】这是不含本月在内的12个月
            // 比如现在是8月，则此接口应返回 去年8月~今年7月的数据
        },
        shippingData: {    // 过去12个月的出库数据
            月份: [第1天的出库量, 第2天的出库量, ......],
            月份: [第1天的出库量, 第2天的出库量, ......],
            // 共计12个月
        }
    }
}
// 请求失败
// ...
```

