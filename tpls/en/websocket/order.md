### order主题

订阅用户的订单更新

订阅规则

主题&市场

订阅该主题必须传apikey

- 支持的市场可以通过api接口[api/v2/exchange/markets](../dex_apis/getMarkets.md) 获取

#### 返回错误码

| 状态码 |                描述                 |
| :---- | :--------------------------------- |
| 104110 | order主题的订阅条件不合法或者不支持 |

#### 推送示例

```json
   {
       "topic": "order&LRC-BTC",
         "ts":1565844328,
       "data": {
         "hash": "11212",
         "clientOrderId": "myOrder",
         "size": "500000000",
         "volume": "210000000",
         "price": "0.000004",
         "filledSize": "30000000",
         "filledVolume": "100000",
         "filledFee": "1000000",
         "status": "processing",
         "createdAt": "1494900087",
         "validSince": "1494900087",
         "validUntil": "1495900087",
         "side": "buy",
         "market": "LRC-BTC"
       }
     }
```

#### 模型

##### 推送数据结构

| 字段  |      类型       | 是否必现 |       说明       |      举例       |
| :--- | :------------- | :------ | :-------------- | :------------- |
| topic |     string      |    是    | 订阅的主题和条件 | "order&lrc-eth" |
|  ts   |     integer     |    是    |     推送时间     |  1584717910000  |
| data  | [Order](#order) |    是    |     订单信息     |        /        |

##### <span id="order">Order数据结构</span>

|     字段      |  类型   | 是否必现 |            说明            |     举例      |
| :----------- | :----- | :------ | :------------------------ | :----------- |
|     hash      | string  |    是    |          订单哈希          |    "11212"    |
| clientOrderId | string  |    是    |        用户自定义id        |   "myOrder"   |
|     size      | string  |    是    |     base token 的数量      |  "500000000"  |
|    volume     | string  |    是    |     quote token 的数量     |  "210000000"  |
|     price     | string  |    是    |          订单价格          |  "0.000004"   |
|  filledSize   | string  |    是    | 已经成交的basetoken的数量  |  "30000000"   |
| filledVolume  | string  |    是    | 已经成交的quotetoken的数量 |   "100000"    |
|   filledFee   | string  |    是    |       已支付的手续费       |   "1000000"   |
|    status     | string  |    是    |          订单状态          | "processing"  |
|   createdAt   | integer |    是    |        订单创建时间        | 1584717910000 |
|   updateAt    | integer |    是    |   订单最后一次的更新时间   | 1584717910000 |
|     side      | string  |    是    |           买或卖           |     "buy"     |
|    market     | string  |    是    |            市场            |   "LRC-ETH"   |

##### 订单状态取值范围

|    状态    |                    说明                    |
| :-------- | :---------------------------------------- |
| processing | 订单进行中, 订单等待成交或者已经成交一部分 |
| processed  |                订单完全成交                |
| cancelling |                   取消中                   |
| cancelled  |                  订单取消                  |
|  expired   |                  订单过期                  |
|  waiting   |                订单还未生效                |
