# 账号金额更新

订阅此主题以接收有关用户余额更新的通知。

## 订阅规则

- 主题名称：`account`
- 订阅该主题是否需要提供ApiKey：是



## 参数列表

该主题不支持任何参数。


## 推送示例

```json
{
    "topic": {
        "topic:": "account"
    },
	"ts":1584717910000,
	"data": {
	    "accountId":1,
	    "totalAmount": "24439253519655",
	    "tokenId": 2,
	    "amountLocked": "0"
	}
}
```

## 模型

#### 推送消息数据结构

| 字段  |        类型         | 必现 |       说明       |     
| :--- | :----------------- | :------ | :-------------- | 
| topic |       JSON        |    是    | 主题和参数 |  
|  ts   |       integer       |    是    |     推送时间（毫秒）     | 
| data  | [Balance](#balance) |    是    |     余额信息     |     

#### <span id= "balance">Balance数据结构</span> 

|     字段     |  类型   | 必现 |    说明    |     
| :---------- | :----- | :------ | :-------- | 
|  accountId   | integer |    是    |   账户ID   |     
|   tokenId    | integer |    是    |   通证ID   |     
| totalAmount  | string  |    是    |  用户余额  | 
| amountLocked | string  |    是    | 冻结的余额 |    

