### Websocket 概述

#### 接入URL

[wss://api.loopring.io/v2/ws](wss://api.loopring.io/v2/ws)

#### 心跳消息

当用户连接到光锥中继的Websocket之后，中继会进行心跳检测，每30s会发送“ping”信息，期待接收客户端的“pong”信息。2分钟未收到回复会自动断开连接。

#### 订阅规则

用户在于光锥中继建立Websocket连接之后，可以订阅消息。需满足以下规则：

1. 用户在取消需要订阅时需要ApiKey的主题时，必须包含相同的ApiKey。
2. 用户可以一次订阅或者取消订阅多个主题，如果订阅的多个主题中有需要ApiKey的，则必须包含ApiKey。
3. 用户可以重复订阅相同的主题，最新的订阅条件会覆盖之前的订阅条件。
4. 用户在一次订阅中，不允许订阅相同的主题

#### 模型

##### 订阅结构

|  字段  |     类型     | 是否必现 |               说明               |                 举例                 |
| :----: | :----------: | :------: | :------------------------------: | :----------------------------------: |
|   op   |    string    |    是    |         订阅或者取消订阅         |                "sub"                 |
| apiKey |    string    |    否    | 订阅要求传ApiKey的主题才是必须的 | “16M2hKHw9b5VuP21YBAJQmCd3VhuNtdDqG” |
|  args  | list<string> |    是    |         订阅的主题及条件         | [ "depth&LRC-ETH&0","trade&LRC-ETH"] |

##### 订阅示例

订阅示例

```json
{
  "op": "sub",
  "args": [
    "candlestick&LRC-BTC&1Hour",
    "depth&LRC-BTC&1",
    "depth10&LRC-BTC&1",
    "trade&LRC-BTC",
    "ticker&LRC-BTC"
  ]
}
```

取消订阅示例

```json
{
  "op": "unSub",
  "args": [
    "candlestick",
    "depth",
    "depth10",
    "trade",
    "ticker"
  ]
}
```

##### 订阅响应结构

|  字段  |     类型     | 是否必现 |               说明               |                 举例                 |
| :----: | :----------: | :------: | :------------------------------: | :----------------------------------: |
|   op   |    string    |    是    |         用户传送来的操作         |                "sub"                 |
| apiKey |    string    |    否    | 订阅要求传ApiKey的主题才是必须的 | “16M2hKHw9b5VuP21YBAJQmCd3VhuNtdDqG” |
|  args  | list<string> |    是    |         订阅的主题及条件         | [ "depth&LRC-ETH&0","trade&LRC-ETH"] |
| result |    [Result](#result)   |    是    |             订阅结果             |                  /                   |

##### 订阅返回示例

订阅成功示例

```json
{
  "op": "sub",
  "apiKey": "",
  "args": [
    "candlestick&LRC-ETH&1hr",
    "depth&LRC-ETH&1",
    "trade&LRC-ETH",
    "ticker&LRC-ETH"
  ],
  "result": {
    "status": "ok"
  }
}
```

订阅条件不合法的失败示例

```json
{
  "op": "sub",
  "apiKey": "",
  "args": [
    "candlestick&LRC-ETH"
  ],
  "result": {
    "status": "failed",
      "error": {
      "code": 104106,
      "message": "receive illegal arg for candlestick:lrc-eth"
    }
  }
}
```

订阅条件无法解析的失败示例

```json
{
  "op": "",
  "apiKey": "",
  "args": [],
  "result": {
    "status": "failed",
    "error": {
      "code": 104115,
      "message": "unexpected msg:xxx"
    }
  }
}
```

#####  <span id="result">Result </span>

|  字段  |      类型       | 是否必现 |         说明         | 举例 |
| :----: | :-------------: | :------: | :------------------: | :--: |
| status |     string      |    是    |     订阅是否成功     | "OK" |
| error  | [Error](#error) |    否    | 订阅失败时的错误信息 |  /   |

##### <span id="error">Error </span>

|  字段   |  类型   | 是否必现 |   说明   |     举例     |
| :-----: | :-----: | :------: | :------: | :----------: |
|  code   | integer |    是    |  错误码  |    107500    |
| message | string  |    是    | 错误信息 | 空的订阅信息 |

#### 公共错误码信息

| **返回码** |                         描述                         |
| :--------: | :--------------------------------------------------: |
|   104100   |                     空的订阅信息                     |
|   104101   | 不支持的操作（光锥中继服务器仅支持sub 和 unsub操作） |
|   104102   |                     不支持的主题                     |
|   104103   |                    重复的订阅主题                    |
|   104104   |                    缺少ApiKey信息                    |
|   104105   |              与之前订阅使用的ApiKey不符              |
|   104112   |                    不合法的ApiKey                    |
|   104113   |               取消订阅未曾订阅过的主题               |
|   104114   |             无法通过APiKey找到对应的用户             |
|   104115   |                  无法识别的订阅消息                  |

### candlestick 主题

订阅candlestick，获取定时推送的candlestick数据的更新消息推送。订阅该主题不需要传ApiKey信息。

#### 订阅格式

主题&市场&间隔

- 支持的市场可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets)获取

- 支持的间隔（interval）为1min, 5min, 15min, 30min, 1hr, 2hr, 4hr, 12hr, 1d, 1w

| 间隔  |  说明  |
| :---: | :----: |
| 1min  | 1分钟  |
| 5min  | 5分钟  |
| 15min | 15分钟 |
| 30min | 30分钟 |
|  1hr  | 1小时  |
|  2hr  | 2小时  |
|  4hr  | 4小时  |
| 12hr  | 12小时 |
|  1d   |  1天   |
|  1w   |  1周   |

#### 返回错误码

| 返回码 |                   描述                    |
| :----: | :---------------------------------------: |
| 104106 | candlestick主题的订阅条件不合法或者不支持 |

#### 推送示例

```json
{
  "topic": "candlestick&lrc-btc&1hr",
  "ts":1584717910000,
  "data": {
    "start": 1584717910000,
    "count":5000,
    "size": "500000000000000000",
    "volume": "2617521141385000000",
    "open": "3997.3",
    "close": "3998.7",
    "high": "4031.9",
    "low": "3982.5"
  }
}
```

#### 模型

##### 推送数据结构

| 字段  |            类型             | 是否必现 |       说明       |          举例           |
| :---: | :-------------------------: | :------: | :--------------: | :---------------------: |
| topic |           string            |    是    | 订阅的主题和条件 | candlestick&lrc-btc&1hr |
|  ts   |           integer           |    时    | 推送时间（毫秒） |      1584717910000      |
| data  | [CandleStick](#candlestick) |    是    | candlestick数据  |            /            |

#####<span id= "candlestick"> CandleStick结构</span>

|  字段  |  类型   | 是否必现 |               说明                |         举例          |
| :----: | :-----: | :------: | :-------------------------------: | :-------------------: |
| start  | integer |    是    |            指开盘时间             |     1584717910000     |
| count  | integer |    是    |             成交笔数              |         5000          |
|  open  | string  |    是    |             开盘价格              |       "3997.3"        |
| close  | string  |    是    |             收盘价格              |       "3998.7"        |
|  high  | string  |    是    |              最高价               |       "4031.9"        |
|  low   | string  |    是    |              最低价               |       "3982.5"        |
|  size  | string  |    是    | 为wei为单位的base token的成交数量 | “500000000000000000”  |
| volume | string  |    是    | 为wei为单位 quote token的成交数量 | "2617521141385000000" |

### depth 主题

订阅深度的主题，获取定时推送的深度信；订阅该主题不需要apiKey；在没有数据更新时，不进行数据推送。

#### 订阅规则

主题&市场&归并等级

- 支持的市场以及市场对应支持的归并等级，可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets) 获取

#### 返回错误码

| 返回码 |                描述                 |
| :----: | :---------------------------------: |
| 104107 | depth主题的订阅条件不合法或者不支持 |

#### 推送示例

```json
{
  "topic": "depth&LRC-ETH&1",
  "ts":1584717910000,
  "startVersion": 1212121,
  "endVersion": "1212123",
  "data": {
    bids: [
      {
        "price": "295.97",
        "size": "456781000000000",
        "volume": "3015000000000",
        "count": 2
      }
    ],
    asks: [
      
    ]
  }
}
```

#### 模型

##### 推送数据结构

|     字段     |      类型       | 是否必现 |         说明         |      举例       |
| :----------: | :-------------: | :------: | :------------------: | :-------------: |
|    topic     |     string      |    是    |   订阅的主题和条件   | depth&LRC-ETH&1 |
|      ts      |     integer     |    是    |       推送时间       |  1584717910000  |
| startVersion |     integer     |    是    | 该次推送的起始版本号 |     1212121     |
|  endVersion  |     integer     |    是    | 该次推送的终结版本号 |     1212123     |
|     data     | [Depth](#depth) |    是    |       深度信息       |        /        |

#####<span id="depth">  Depth数据结构</span>

| 字段 | 类型                                                         | 是否必现 | 说明     | 举例 |
| ---- | ------------------------------------------------------------ | -------- | -------- | ---- |
| bids | list< [Slot](#slot) > | 是       | 买单深度 | /    |
| asks | list< [Slot](#slot) > | 是       | 卖单深度 | /    |

#### <span id = "slot">Slot</span>

每一条深度数据

| 字段   | 类型    | 是否必现 | 说明           | 举例     |
| ------ | ------- | -------- | -------------- | -------- |
| price  | string  | 是       | 价格           | 0.002    |
| size   | string  | 是       | 挂单量         | 21000    |
| volume | string  | 是       | 挂单总量       | 33220000 |
| count  | integer | 是       | 聚合的订单数目 | 4        |

#### 如何构建本地的Orderbook

1. 订阅 depth主题

2. 开始缓存收到的更新。同一个价位，后收到的更新覆盖前面的。

3. 访问接口 https://api.loopring.io/api/v1/depth 获得一个全量的深度快照。

4. 3中获取的快照如果version大约本地version（endVersion），则直接覆盖，如果小于本地version，则相同的价格不覆盖，不同的价格则覆盖。

5. 将深度快照中的内容更新到本地orderbook副本中，并从websocket接收到的第一个startVersion <=本地 version+1 且 endVersion >= 本地version 的event开始继续更新本地副本。

6. 每一个新推送的startVersion应该恰好等于上一个event的endVersion+1，否则可能出现了丢包，请从step3重新进行初始化

7. 每一个推送中的挂单量代表这个价格目前的挂单量绝对值，而不是相对变化。

8. 如果某个价格对应的挂单量为0，表示该价位的挂单已经撤单或者被吃，应该移除这个价位。

### depth10 主题

  获取定时推送的当前深度中卖单和买单的前10条数据。该订阅不需要apikey，有无数据都会进行推送。

####   订阅规则：

​	主题&市场&归并等级

- 支持的市场以及市场对应支持的归并等级，可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets) 获取

#### 返回错误码

| 返回码 |                 描述                  |
| :----: | :-----------------------------------: |
| 104108 | depth10主题的订阅条件不合法或者不支持 |

####   订阅推送示例

  ```json
{
  "topic": "depth10&LRC-BTC&1",
  "ts": 1584717910000,
  "data": {
    "bids": [
      {
        "price": "295.97",
        "size": "4567810000000000",
        "volume": "30150000000000",
        "count": 2
      }
    ],
    "asks": [
      {
        "price": "298.97",
        "size": "456781000000000000",
        "volume": "301500000000000",
        "count": 2
      }
    ]
  }
}
  ```

#### 模型

##### 推送数据结构

| 字段  |      类型       | 是否必现 |       说明       |       举例        |
| :---: | :-------------: | :------: | :--------------: | :---------------: |
| topic |     string      |    是    | 订阅的主题和条件 | depth10&LRC-ETH&1 |
|  ts   |     integer     |    是    |     推送时间     |   1584717910000   |
| data  | [Depth](#depth) |    是    |     深度信息     |         /         |

### trade 主题

订阅该主题，获取定时的最新的成交信息；没有更新则不推送

#### 订阅规则

主题&市场

- 支持的市场可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets) 获取

#### 返回错误码

| 返回码 |                描述                 |
| :----: | :---------------------------------: |
| 104109 | trade主题的订阅条件不合法或者不支持 |

#### 订阅推送示例

```json
   {
       "topic": "trade&LRC-ETH",
       "ts":1584717910000,
       "data": {
         "timestamp": 1584717910000,
         "tradeId": 123456789,
         "side": "buy",
         "size": "500000",
         "price": "0.0008",
         "fee":"100"
       }
     }
```

#### 模型

##### 推送数据结构

|  字段   |      类型       | 是否必现 |       说明       |     举例      |
| :-----: | :-------------: | :------: | :--------------: | :-----------: |
|  topic  |     string      |    是    | 订阅的主题和条件 | trade&LRC-ETH |
| integer |     integer     |    是    |     推送时间     | 1584717910000 |
|  data   | [Trade](#trade) |    是    |     深度信息     |       /       |

##### <span id="trade">Trade 数据结构</span>

|   字段    |      类型       | 是否必现 |       说明       |     举例      |
| :-------: | :-------------: | :------: | :--------------: | :-----------: |
| timestamp |   integer |    是    | 成交时间 | 1584717910000 |
|  tradeId  | integer |    是    |       交易编号       |   123456789   |
|   side    | string  |    是    |  买或者卖，指taker   | "buy" |
|   size    | string  |    是    | base token的成交数量 | "500000" |
|   price   | string  |    是    |       成交价格       | "0.0008" |
|    fee    | string  |    是    |   base token的收费   | "100" |

### ticker 主题

订阅以获得定时推送的最新的ticker信息，没有更新则不推送

#### 订阅规则

主题&市场

- 支持的市场可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets) 获取

####  返回错误码

| 返回码 |                 描述                 |
| :----: | :----------------------------------: |
| 104111 | ticker主题的订阅条件不合法或者不支持 |

#### 订阅推送示例

```json
{
  "topic": "ticker&LRC-ETH",
  "ts": 1584717910000,
  "data": {
    "market":"LRC-ETH",
    "timestamp": 1584717910000,
    "size": "5000000",
    "volume":"1000",
    "open": "0.0002",
    "high": "0.00025",
    "low": "0.0002",
    "close": "0.00025",
    "count": 5000,
    "bid": "0.00026",
    "ask": "0.00027"
  }
}
```

#### 模型

##### 订阅推送模型

|  字段   |       类型        | 是否必现 |       说明       |      举例      |
| :-----: | :---------------: | :------: | :--------------: | :------------: |
|  topic  |      string       |    是    | 订阅的主题和条件 | ticker&LRC-ETH |
| integer |      integer      |    是    |     推送时间     | 1584717910000  |
|  data   | [Ticker](#ticker) |    是    |     深度信息     |       /        |

##### <span id="ticker">Ticker数据结构</span>

|   字段    |  类型   | 是否必现 |         说明         |     举例      |
| :-------: | :-----: | :------: | :------------------: | :-----------: |
|  market   | string  |    是    |         市场         |   "LRC-ETH"   |
| timestamp | integer |    是    |    ticker生成时间    | 1584717910000 |
|   size    | string  |    是    |  base token的成交量  |   "5000000"   |
|  volume   | string  |    是    | quote token 的成交量 |    "1000"     |
|   open    | string  |    是    |        开盘价        |   "0.0002"    |
|   high    | string  |    是    |        最高价        |   0.00025"    |
|    low    | string  |    是    |        最低价        |   "0.0002"    |
|   close   | string  |    是    |      最新成交价      |   "0.00025"   |
|   count   | integer |    是    |       成交笔数       |     5000      |
|    bid    | string  |    是    |      买单最高价      |   "0.00026"   |
|    ask    | string  |    是    |      卖单最低价      |   "0.00027"   |

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
| topic |       string        |    是    | 订阅的主题和条件 |    account    |
|  ts   |       integer       |    是    |     推送时间     | 1584717910000 |
| data  | [Balance](#balance) |    是    |     余额信息     |       /       |

##### <span id= "balance">Balance</span> 数据结构

|     字段     |  类型   | 是否必现 |    说明    |       举例       |
| :----------: | :-----: | :------: | :--------: | :--------------: |
|  accountId   | integer |    是    |   用户Id   |        1         |
|   tokenId    | integer |    是    |   通证Id   |        2         |
| totalAmount  | string  |    是    |  用户余额  | "24439253519655" |
| frezeeAmount | string  |    是    | 冻结的余额 |       "0"        |

### order主题

订阅用户的订单更新

订阅规则

主题&市场

订阅该主题必须传apikey

- 支持的市场可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets) 获取

#### 返回错误码

| 返回码 |                描述                 |
| :----: | :---------------------------------: |
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

| 字段  |      类型       | 是否必现 |       说明       |     举例      |
| :---: | :-------------: | :------: | :--------------: | :-----------: |
| topic |     string      |    是    | 订阅的主题和条件 |    account    |
|  ts   |     integer     |    是    |     推送时间     | 1584717910000 |
| data  | [Order](#order) |    是    |     订单信息     |       /       |

##### <span id="order">Order数据结构</span>

|     字段      |  类型   | 是否必现 |            说明            |     举例      |
| :-----------: | :-----: | :------: | :------------------------: | :-----------: |
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
| :--------: | :----------------------------------------: |
| processing | 订单进行中，订单等待成交或者已经成交一部分 |
| processed  |                订单完全成交                |
| cancelling |                   取消中                   |
| cancelled  |                  订单取消                  |
|  expired   |                  订单过期                  |
|  waiting   |                订单还未生效                |

 		   