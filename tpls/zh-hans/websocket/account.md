# 账号金额更新

订阅此主题以接收有关用户余额更新的通知。

## 订阅规则

- 主题名称：`account`
- 订阅该主题是否需要提供ApiKey：是



## 参数列表

该主题支持一个可选的`v3`标记，用于表示是否订阅`v3`格式，即包含NFT信息的消息。

|  Parameter |  Required |              Note                |
| :---- | :--- |:--------------------------------- |
| accountId | N | apiKey绑定了account,因此不必传 |
| v3 | N | 是否订阅`v3`格式，默认为否，即兼容之前的订阅格式 |



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

如果是`v3`消息

| 字段  |        类型         | 必现 |       说明       |
| :--- | :----------------- | :------ | :-------------- |
| topic |       JSON        |    是    | 主题和参数 |
|  ts   |       integer       |    是    |     推送时间（毫秒）     |
| data  | [BalanceV3](#balanceV3) |    是    |     余额信息(包含NFT信息)     |

否则和之前一样

| 字段  |        类型         | 必现 |       说明       |
| :--- | :----------------- | :------ | :-------------- |
| topic |       JSON        |    是    | 主题和参数 |
|  ts   |       integer       |    是    |     推送时间（毫秒）     |
| data  | [Balance](#balance) |    是    |     余额信息     |

#### <span id= "balanceV3">BalanceV3</span> 

|     Field     |  Type   | Required |    Note    |
| :---------- | :----- | :------ | :-------- |
|  accountId   | integer |    Y    |   Account ID   |
|   tokenId    | integer |    Y    |   Token ID   |
| total  | string  |    Y    |  Total token balance  |
| locked | string  |    Y    | Token balance locked by orders |
| nftId  | string  |    N    |  NFT ID if it's NFT token  |
| nftData | string  |    N    | NFT hash data if it's NFT token |
| tokenAddress  | string  |    N    |  Nft token address if it's NFT token  |

#### <span id= "balance">Balance数据结构</span> 

|     字段     |  类型   | 必现 |    说明    |
| :---------- | :----- | :------ | :-------- |
|  accountId   | integer |    是    |   账户ID   |
|   tokenId    | integer |    是    |   通证ID   |
| totalAmount  | string  |    是    |  用户余额  |
| amountLocked | string  |    是    | 冻结的余额 |
