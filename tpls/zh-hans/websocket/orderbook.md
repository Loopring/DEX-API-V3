# 订单簿更新


订阅此主题以接收特定交易对定单薄更新的通知。


## 订阅规则

- 主题名称：`orderbook`
- 订阅该主题是否需要提供ApiKey：否


## 参数列表

| 参数名|  必现 |             描述                 |
| :---- | :------ |:--------------------------------- |
| market | 是 | 交易对（支持的交易对可以通过api接口[api/v2/exchange/markets](../dex_apis/getMarkets.md)获取）|
| level | 是 | 深度聚合级别 |
| count | 是 | 买卖深度条目数量，值不可以超过50。仅在snapshot = true时生效 |
| snapshot |否 | 默认为false。 如果该值为true，并且当深度条目有任何一条变化，那么指定数量的深度条目会被全量推送给客户端。 |

## 状态码

| 状态码 |                描述                 |
| :---- | :--------------------------------- |
| 104107 | 主题或参数非法|

## 推送示例

```json
{
    "topic": {
        "topic:": "orderbook",
        "market": "LRC-USDT",
      	"level": 0,
        "count": 20,
        "snapshot": true
    },
    "ts": 1584717910000,
    "startVersion": 1212121,
    "endVersion": "1212123",
    "data": {
        "bids": [
            [
                "295.97",  //price
                "456781000000000",  //size
                "3015000000000",  //volume
                "4"  //count
            ]
        ],
        "asks": [
            [
              "298.97",
              "456781000000000000",
              "301500000000000",
              "2"
            ]
        ]
    }
}
```

## 模型

#### 推送消息数据结构

|     字段     |      类型       | 必现 |         说明         |
| :---------- | :------------- | :------ | :------------------ |
| topic |       JSON        |    是    | 主题和参数 |
|      ts      |     integer     |    是    |       推送时间（毫秒）       |
| startVersion |     integer     |    是    | 该次推送的起始版本号 |
|  endVersion  |     integer     |    是    | 该次推送的终结版本号 |
|     data     | [Orderbook](#orderbook) |    是    |       订单簿信息       |

####<span id="orderbook">Orderbook数据结构</span>

| 字段 | 类型                           | 必现 | 说明     |
| :---- | :------------------------------ | :-------- | :-------- |
| bids | List\[List\[string\]] | 是       | 代表买单深度的[PriceSlot](#slot)数组列表 |
| asks | List\[List\[string\]]| 是       | 代表卖单深度的[PriceSlot](#slot)t数组列表 |

#### <span id = "slot">PriceSlot数组</span>

| 序号  | 类型   | 必现 | 说明           |
| :------ | :------ | :-------- | :-------------- | :|
|    1     | string | 是       | 价格           |
|    2     | string | 是       | 数量（基础通证的数量）         |
|    3     | string | 是       | 成交额（ 计价通证的数量）  |
|    4     | string | 是       | 聚合的订单数目 |


需要注意的是，每一个推送中的数量和成交额代表这个价格目前的数量和成交额的绝对值，而不是相对变化。

## 构建本地订单簿

您可以通过下列步骤构建本地订单簿：

1. 订阅 orderbook主题。
2. 开始缓存收到的更新。同一个价位，后收到的更新覆盖前面的。
3. 访问接口 [api/v1/depth](../dex_apis/getDepth.md) 获得一个全量的深度快照。
4. 3中获取的快照如果`version`大于本地`version`（`endVersion`），则直接覆盖，如果小于本地version，则相同的价格不覆盖，不同的价格则覆盖。
5. 将深度快照中的内容更新到本地订单簿副本中，并从WebSocket接收到的第一个`startVersion` <=本地 `version + 1` 且 endVersion >= 本地version 的event开始继续更新本地副本。
6. 每一个新推送的`startVersion`应该恰好等于上一个event的`endVersion + 1`，否则可能出现了丢包，请从step3重新进行初始化。
7. 如果某个价格对应的挂单量为0，表示该价位的挂单已经撤单或者被吃，应该移除这个价位。

