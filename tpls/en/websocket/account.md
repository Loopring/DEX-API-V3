# 订阅用户账号金额更新


通过订阅该主题，您可以获得用户余额和冻结金额更新的数据推送。

## 订阅规则

- `topic`需要设为`account`。
- 订阅该主题**需要提供ApiKey**。

## 推送示例

```json
{
	"topic": "account",
	"ts":1584717910000,
	"data": {
	    "accountId":1,
	    "totalAmount": "24439253519655",
	    "tokenId": 2,
	    "frezeeAmount": "0"
	}
}
```

## 模型

#### 推送数据结构

| 字段  |        类型         | 必现 |       说明       |     举例      |
| :--- | :----------------- | :------ | :-------------- | :----------- |
| topic |       string        |    是    | 订阅的主题和条件 |   "account"   |
|  ts   |       integer       |    是    |     推送时间     | 1584717910000 |
| data  | [Balance](#balance) |    是    |     余额信息     |       /       |

#### <span id= "balance">Balance数据结构</span> 

|     字段     |  类型   | 必现 |    说明    |       举例       |
| :---------- | :----- | :------ | :-------- | :-------------- |
|  accountId   | integer |    是    |   用户Id   |        1         |
|   tokenId    | integer |    是    |   通证Id   |        2         |
| totalAmount  | string  |    是    |  用户余额  | "24439253519655" |
| frezeeAmount | string  |    是    | 冻结的余额 |       "0"        |

