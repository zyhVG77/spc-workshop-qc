## /api/workshop/getRelationshipForm

描述：获取用户与车间之间的绑定信息

请求方式：GET

输入：

```
{
  “userid”:the id of the current user
}
```

输出：

```
// 获取成功
{
    status: 'success',
    relationshipform: [
        {
            workshopid:'id of the workshop that bond with the user'
        },
        {
            /*
            	The same content as above
            */
        },
        // ......
    ]
}
// 获取失败
{
    status: 'fail',
    errorMsg: 'reason or something'
}
```



## /api/user/getUserId

描述：获取所有存在的用户id

请求方式：GET

输入：无

输出：

```
// 获取成功
{
    status: 'success',
    userid: [
        {
            id: 'id of the suers',
            checkrole:'role of the user'
        },
        {
            /*
            	The same content as above
            */
        },
        // ......
    ]
}
// 获取失败
{
    status: 'fail',
    errorMsg: 'reason or something'
}
```

## /api/workshop/getAllWorkshopsId

描述：获取所有存在的车间id

请求方式：GET

输入：无

输出：

```
// 获取成功
{
    status: 'success',
    workshopid: [
        {
            id: 'id of the workshop',
        },
        {
            /*
            	The same content as above
            */
        },
        // ......
    ]
}
// 获取失败
{
    status: 'fail',
    errorMsg: 'reason or something'
}
```

## /api/user/submitRelatonship

描述：提交用户管理内容

请求方式：POST

输入：

```
myform:{
              checkrole: "the role of the user",
              userid:"the id of the user",
              mordify:"whether the user is a new one or not",
              relations: [
                  {
                      workshopId: "id of the workshop",
                      checked: "whether the user manages the workshop or not"
                  },
                  {
                      workshopId: "车间二",
                      checked: false
                  },
                  {
                      workshopId: "车间四",
                      checked: false
                  },
                   {
                      /*
            	      The same content as above
                      */
                  },
              ]
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

