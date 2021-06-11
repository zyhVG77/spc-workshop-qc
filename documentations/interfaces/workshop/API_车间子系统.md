## 接口的一点增补

### /api/user/GetUserInfo

说明：获取用户信息

请求方式：GET

输入：

```json
{
    Authentication: 'token' // 位于请求头中
}
```

输出：

```json
// 获取成功
{
    status: 'success',
    user: {
        id: "id",
        username: "username",
        email: "an email address",
        fullname: "fullname",
        workId: "id used in factory",
        avatar: "the avatar image path",
        role: "role" // admin | super_editor | viewer
    }
}
// 获取失败
{
    status: 'fail',
    errorMsg: 'reason or something else'
}
```



### /api/workshop/GetReportDetailHtml

说明：获取异常报告的HTML网页

请求方式：GET

输入：

```json
{
	Authentication: 'token', // 位于请求头中
    id: 'report id'
}
```

输出：

```json
// 获取成功
{
    status: 'success',
    content: 'html string'
}
// 获取失败
{
    status: 'fail',
    errorMsg: 'reason or something else'
}
```

___

## 接口一览

我按照index.js中的接口定义进行了一些实现, 并且做了一些增删改如下

接口的路由信息在SPC/interface/urls.py中, 接口的具体实现在SPC/util/interface.py中

所有最新更改都已上传到网盘SPC中, 代码还未进行测试

#### ModifyPassword: (未实现)

#### UpdateUserInfo: (未实现)

#### ConfirmLogin: (未实现)

```
input:
{
	'username','password','rememberMe'
}
output:
{
	'user':{
		'id':userId,
		'username':userName,
		'email':email,
		'fullname':fullname,
		'word_id':workId,
		'avatar':avatar,
		'role':role,
	},
	'status':状态信息,
	'token':token
}
```

状态返回时, 如正常, 则返回'success', 如异常, 则返回异常信息字符串, 返回异常信息时, 其他内容将无法被返回

```
#正常状态
{'status':'success'}
#异常状态
{'status':异常信息}
```

#### GetAllProducts

```
input:
{'token':token}
output:
{
	'status':status,
	'products':[
		{
			'id','name','type','description',
			'parameters':[
				{
					'id','name','value_type','scale','unit','description','usl','lsl',
					'graph_type': 控制图类型
					'control_plan_id': 控制计划编号,需要使用控制计划编号和测量计划编号来访问控图
				},
				...
			],
			'workshop':[
				{'measure_plan_id': 测量计划编号,用于区分不同车间},
				...
			]
		},
		...
	]
}
```

#### SubmitProduct

```
input:
{
	'token':token,
    'product':{
        'id':modify=False时无需指定,
        'name','type','description',
        'parameters':[
            {
                'id':modify=False时无需指定,
                'name','scale','unit','description','usl','lsl',
                'value_type':modify=True时无需指定,因为其在参数确定后无法修改
                'graph_type': 控制图类型,
            },
        ...
        ],
    },
    'modify':bool
}
更改:
1.	modify key: 'productForm'->'product'
2.	modify key: 'spc_model'->'graph_type'

output:
{
	'status':status,
    'product':{
        'id','name','type','description',
        'parameters':[
            {
                'id','name','value_type','scale','unit','description','usl','lsl',
                'graph_type': 控制图类型
                'control_plan_id': 控制计划编号,需要使用控制计划编号和测量计划编号来访问控图
            },
            ...
        ],
        'workshop':[
            {'measure_plan_id': 测量计划编号,用于区分不同车间},
            ...
        ]
    }
}
```

在修改过程中发生错误时, 会有一些修改已经得到保存而另一些修改还没执行, 此时接口除了会返回错误信息'status'之外, 'product'键值对也会被返回, 让用户可以看见哪些信息修改成功而哪些失败了

如果由于id或者其他问题导致product本身无法被获得, 则接口只会返回'status'信息

#### DeleteProduct

```
input:
{
	'token':token,
	'product_id':productId,
}
output:
{'status':status}
```

#### /api/workshop/GetControlGraph

```
input:
{
	'token':token,
	'control_plan_id':控制计划编号,
	'measure_plan_id':测量计划编号,
	'start_time':起始时间,如果为默认视图则不应包含该项,
	'end_time':终止时间,如果为默认视图则不应包含该项,
	'tmp_point_id':当前最新点,需要持续更新图表则应指定该项(仅当不包含end_time时控制图可以动态更新),
	'analyze':bool,是否返回控制图的分析结果,如果为True则返回当前控制图的异常信息Html网页
}
output:
//analyze:False
{
	'status':status,
	'updated':bool,表示是否更新,为False时'options'项不被包含
	'options':options,详见SPC/util/charts, 更新时依然返回整个options
	'tmp_point_id':当前最新点编号
}
//analyze:True
(未实现)
```

#### GetAllExceptionReports

```
input:
{'token':token}
output:
{
	'status':status,
	'reports':[
		{
			    'id':异常信息编号,用于查看详情,
                'product':产品名,
                'parameter':参数名,
                'measure_plan':测量计划编号(和车间相关),
                'measure_form_id':异常点编号,
                'time':异常时间,
                'information':异常信息字符串,
                'read':bool值,是否已读
		}
	],
}
```

#### MarkReportAsRead

```
input:
{
	'token':token,
	'abnormality_info_id':异常信息编号
}
outpot:
{
	'status':status
}
```

#### /api/workshop/GetDetailReport (未实现)

```
input:
{
	'token':token,
	'abnormality_info_id':异常信息编号
}
outpot:
详细异常信息的html网页
```

