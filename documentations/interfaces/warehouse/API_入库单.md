## /PutInForm/submitPutInForm

描述：提交入库单

请求方式：POST

输入：

```
{
  putInForm:{
				inputDate:"入库日期",
				seller:"供货商",
				qualityChecker:"质检员",
				holder:"保管员",
				passer:"经手人",
				manager:"主管",
				accountant:"会计",
				autodistribute:"是否自动分配储位",
				parameters:[
				{
				index:"编号", compName:"零件名称", model:"规格", unit:"单位", quantity:"数量", price:"单价", totalPrice:"总价", comment:"备注",
				}，
				{
				/*The same content as above*/
				},
				// ......
				]
				
			}
			
}
```

输出：

```
// 获取成功
{
    status: 'success'
}
// 获取失败
{
    status: 'fail',
    errorMsg: 'reason or something'
}
```

