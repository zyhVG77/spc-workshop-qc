# API—仓位图

### 1 Get Storage Cells

**请求地址**：/api/warehouse/GetStorageCells 

**说明**：获取储位信息

**请求方式**：GET

**输入**：

```json
{
    order: 0
    // order=0: 默认排序（）
    // order=1: 空闲数量从大到小
    // order=2: 空闲数量从小到大
    page: 1, // 页码，每页100个，从第一页开始
    warehouse_id: 'id of warehouse', // 仓库编号
    // 仓库编号特殊值：warehouse_id='all'代表全部仓库
}
```

**输出**：

```json
// 请求成功，
{
    status: 'success',
    storage_cells: [
        {
            id: 'id of the cell',
            warehouse_id: 'id of the warehouse the cell belongs to',
            capacity: 100, // 储位容量
            occupy: 40, // 当前占用
        }
    ]
}

// 请求失败
{
    status: 'fail',
    errorMsg: 'reason or something else'
}
```

### 2 Get Warehouse Info

**请求地址**：/api/warehouse/GetWarehouseInfo

**说明**：获取所有的仓库信息

**请求方式**：GET

**输入**：

```json
{}
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    warehouses: [
        {
            id: 'id of the warehouse',
            name: 'name of the warehouse'
        },
        {
            // ...
        },
        // ...
    ]
}
// 请求失败
// ......
```

### 3 Get Number Of Storage Cells

**请求地址**：/api/warehouse/GetNumberOfStorageCells

**说明**：获取全部或某一库房储位数量

**请求方式**：GET

**输入**：

```json
{
    warehouse_id: 'id the of warehouse'
    // 特殊值：warehouse_id='all'，同上
}
```

**输出**：

```json
// 请求成功
{
    status: 'success',
    number: 50 // 储位数量
}
// 请求失败
// ......
```

### 4  Get Storage Cell Detail

**请求地址**：/api/warehouse/GetStorageCellDetail

**说明**：获取某一储位的信息

**请求方式**：GET

**输入**：

```json
{
    id: 'id of the storage cell'
}
```

**输出**：

```json
// 请求成功
{
    statue: 'success',
    detail: {
        id: 'id of the cell',
        warehouse_id: 'id of the warehouse the cell belongs to',
        capacity: 200, // 容量
        occupy: 50, // 占用
        products: [
            {
                id: 'id of the product',
                name: 'name of the product',
                quantity: 'quantity of the product',
                start_time: 'start time of store'
            },
            {
                // ...
            },
            // ...
        ]
    }
}
// 请求失败
// ......
```
