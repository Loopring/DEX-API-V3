#### Account 主题

订阅用户的余额和冻结金额相关的信息

#### 订阅规则

主题即Account

订阅该主题必须传Apikey

#### 订阅推送示例

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

#### 模型

##### 订阅推送数据结构

| 字段  |        类型         | 是否必现 |       说明       |     举例      |
| :---: | :-----------------: | :------: | :--------------: | :-----------: |
| topic |       string        |    是    | 订阅的主题和条件 |   "account"   |
|  ts   |       integer       |    是    |     推送时间     | 1584717910000 |
| data  | [Balance](#balance) |    是    |     余额信息     |       /       |

##### <span id= "balance">Balance</span> 数据结构

|     字段     |  类型   | 是否必现 |    说明    |       举例       |
| :----------: | :-----: | :------: | :--------: | :--------------: |
|  accountId   | integer |    是    |   用户Id   |        1         |
|   tokenId    | integer |    是    |   通证Id   |        2         |
| totalAmount  | string  |    是    |  用户余额  | "24439253519655" |
| frezeeAmount | string  |    是    | 冻结的余额 |       "0"        |

